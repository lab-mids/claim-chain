"""Convert a PDF into a claim-chain YAML with Claude, validating and repairing the result."""
import base64
import datetime
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import anthropic
import yaml

from claimchain.resources import data_path, read_prompt, schema_path
from claimchain.validate import dump_chain, normalize, schema_version, validate_chain

DEFAULT_MODEL = "claude-opus-5-5"
DEFAULT_EFFORT = "high"
MAX_PDF_BYTES = 32 * 1024 * 1024  # request size limit for base64 PDF input
FALLBACK_BETA = "server-side-fallback-2026-07-01"
YAML_BLOCK = re.compile(r"```ya?ml\s*\n(.*?)```", re.DOTALL)


class ConversionError(RuntimeError):
    """The model could not produce a chain (refusal, truncation, unreadable input)."""


@dataclass
class ConversionResult:
    chain: dict
    yaml_text: str
    issues: list[str]  # empty when the chain validates
    attempts: int
    usage: dict = field(default_factory=dict)

    @property
    def valid(self) -> bool:
        return not self.issues


def system_prompt() -> list[dict]:
    """Instructions, checklist, schema and reference example. Identical for every paper, so it is cached."""
    text = "\n\n".join([
        read_prompt("instructions.md"),
        read_prompt("review-checklist.md"),
        "# LinkML schema (claim_chain.yaml)\n\n```yaml\n" + schema_path().read_text(encoding="utf-8") + "```",
        "# Reference example of a complete, validated chain\n\n```yaml\n"
        + data_path("example.yaml").read_text(encoding="utf-8") + "```",
    ])
    return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]


def first_message(pdf: Path) -> dict:
    data = pdf.read_bytes()
    if len(data) > MAX_PDF_BYTES:
        raise ConversionError(f"{pdf} is {len(data) / 2**20:.1f} MB; the API accepts PDFs up to 32 MB")
    return {"role": "user", "content": [
        {"type": "document",
         "source": {"type": "base64", "media_type": "application/pdf",
                    "data": base64.standard_b64encode(data).decode("ascii")},
         "cache_control": {"type": "ephemeral"}},  # reused unchanged by every repair round
        {"type": "text",
         "text": f"Encode the attached paper (file name: {pdf.name}) as a claim chain. "
                 "Reply with the complete ArgumentChain in one ```yaml block and nothing else."},
    ]}


def parse_reply(text: str) -> tuple[dict | None, list[str]]:
    blocks = YAML_BLOCK.findall(text)
    if not blocks:
        return None, ["the reply contains no ```yaml block"]
    try:
        chain = yaml.safe_load(max(blocks, key=len))
    except yaml.YAMLError as exc:
        return None, [f"YAML does not parse: {exc}"]
    if not isinstance(chain, dict):
        return None, ["the YAML block is not a mapping (ArgumentChain)"]
    return chain, []


def fill_header(chain: dict, model: str) -> dict:
    from claimchain import __version__
    chain["schema_version"] = schema_version()
    chain["annotator"] = f"claimchain {__version__} ({model})"
    chain["annotation_date"] = datetime.date.today().isoformat()
    return chain


def repair_message(issues: list[str]) -> dict:
    listed = "\n".join(f"- {i}" for i in issues[:50])
    more = f"\n- ... and {len(issues) - 50} more" if len(issues) > 50 else ""
    return {"role": "user", "content":
            f"The chain you returned has these problems:\n{listed}{more}\n\n"
            "Fix all of them and reply with the complete corrected ArgumentChain in one ```yaml block."}


def _ask(client, *, model, effort, fallback, max_tokens, system, messages):
    kwargs = dict(model=model, max_tokens=max_tokens, system=system, messages=messages,
                  thinking={"type": "adaptive"}, output_config={"effort": effort})
    if fallback:
        # On a policy decline, the API re-runs the request on Anthropic's recommended fallback model.
        stream = client.beta.messages.stream(betas=[FALLBACK_BETA], fallbacks="default", **kwargs)
    else:
        stream = client.messages.stream(**kwargs)
    with stream as s:
        return s.get_final_message()


def convert_pdf(
    pdf: str | Path,
    *,
    client: anthropic.Anthropic | None = None,
    model: str = DEFAULT_MODEL,
    effort: str = DEFAULT_EFFORT,
    max_repairs: int = 2,
    fallback: bool = True,
    max_tokens: int = 128000,
    log: Callable[[str], None] = lambda msg: None,
) -> ConversionResult:
    """Encode `pdf` as a claim chain.

    Claude reads the PDF (text and figures) and returns YAML. The YAML is normalized and
    validated against the schema; remaining problems are sent back for up to `max_repairs`
    correction rounds. The last result is returned even if problems remain (see `issues`).
    """
    pdf = Path(pdf)
    client = client or anthropic.Anthropic()
    system = system_prompt()
    messages = [first_message(pdf)]
    usage = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0}
    chain, issues = None, []

    for attempt in range(1, max_repairs + 2):
        log(f"{pdf.name}: request {attempt} to {model}")
        msg = _ask(client, model=model, effort=effort, fallback=fallback,
                   max_tokens=max_tokens, system=system, messages=messages)
        for key in usage:
            usage[key] += getattr(msg.usage, key, 0) or 0

        if msg.stop_reason == "refusal":
            raise ConversionError(f"the model declined to process {pdf.name}")
        if msg.stop_reason == "max_tokens":
            raise ConversionError(f"the reply for {pdf.name} hit max_tokens={max_tokens} and is incomplete")

        text = "".join(b.text for b in msg.content if b.type == "text")
        parsed, issues = parse_reply(text)
        if parsed is not None:
            chain = fill_header(normalize(parsed), model)
            issues = validate_chain(chain)
        log(f"{pdf.name}: {len(issues)} problem(s) after request {attempt}")
        if not issues:
            break
        # Append the full reply (thinking blocks included) and ask for a corrected version.
        messages += [{"role": "assistant", "content": msg.content}, repair_message(issues)]

    if chain is None:
        raise ConversionError(f"no parsable chain for {pdf.name}: {'; '.join(issues)}")
    return ConversionResult(chain=chain, yaml_text=dump_chain(chain), issues=issues,
                            attempts=attempt, usage=usage)
