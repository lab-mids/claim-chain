"""Offline tests: a fake client stands in for the Claude API."""
import copy
from types import SimpleNamespace

import pytest
import yaml

import claimchain.convert as convert_mod
from claimchain import cli, convert_pdf, validate_chain
from claimchain.resources import data_path
from claimchain.validate import dump_chain, normalize

EXAMPLE = yaml.safe_load(data_path("example.yaml").read_text(encoding="utf-8"))


def reply(chain_or_text, stop_reason="end_turn"):
    text = chain_or_text if isinstance(chain_or_text, str) else "```yaml\n" + yaml.safe_dump(chain_or_text, sort_keys=False) + "```"
    return SimpleNamespace(
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=text)],
        stop_reason=stop_reason,
        usage=SimpleNamespace(input_tokens=100, output_tokens=50, cache_read_input_tokens=10),
    )


class FakeStream:
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.msg


class FakeClient:
    """Returns the queued replies in order and records every request."""

    def __init__(self, *replies):
        self.replies = list(replies)
        self.requests = []
        self.messages = SimpleNamespace(stream=self._stream)
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self._stream))

    def _stream(self, **kwargs):
        self.requests.append(copy.deepcopy({k: v for k, v in kwargs.items() if k != "system"}))
        return FakeStream(self.replies.pop(0))


@pytest.fixture
def pdf(tmp_path):
    path = tmp_path / "2601.00001.pdf"
    path.write_bytes(b"%PDF-1.4 test")
    return path


def broken_chain():
    chain = copy.deepcopy(EXAMPLE)
    claim = next(s for s in chain["statements"] if s["statement_type"] == "CLAIM")
    del claim["assessment"]
    return chain, claim["id"]


def test_example_is_valid():
    assert validate_chain(copy.deepcopy(EXAMPLE)) == []


def test_valid_reply_needs_one_request(pdf):
    client = FakeClient(reply(EXAMPLE))
    result = convert_pdf(pdf, client=client)
    assert result.valid and result.attempts == 1
    req = client.requests[0]
    assert req["model"] == "claude-opus-5-5"
    assert req["fallbacks"] == "default" and req["betas"] == ["server-side-fallback-2026-07-01"]
    assert req["messages"][0]["content"][0]["type"] == "document"
    assert result.chain["annotator"].startswith("claimchain ")
    assert result.usage["input_tokens"] == 100


def test_repair_round_sends_problems_back(pdf):
    bad, claim_id = broken_chain()
    client = FakeClient(reply(bad), reply(EXAMPLE))
    result = convert_pdf(pdf, client=client)
    assert result.valid and result.attempts == 2
    second = client.requests[1]["messages"]
    assert [m["role"] for m in second] == ["user", "assistant", "user"]
    assert claim_id in second[-1]["content"]


def test_problems_remain_after_max_repairs(pdf):
    bad, _ = broken_chain()
    result = convert_pdf(pdf, client=FakeClient(reply(bad), reply(bad)), max_repairs=1)
    assert not result.valid and result.attempts == 2
    assert any("has no assessment" in i for i in result.issues)


def test_no_yaml_block_then_fixed(pdf):
    result = convert_pdf(pdf, client=FakeClient(reply("Here is my analysis."), reply(EXAMPLE)))
    assert result.valid and result.attempts == 2


def test_refusal_raises(pdf):
    with pytest.raises(convert_mod.ConversionError):
        convert_pdf(pdf, client=FakeClient(reply("", stop_reason="refusal")))


def test_no_fallback_uses_plain_endpoint(pdf):
    client = FakeClient(reply(EXAMPLE))
    convert_pdf(pdf, client=client, fallback=False)
    assert "fallbacks" not in client.requests[0]


def test_normalize_fixes_common_yaml_slips():
    chain = copy.deepcopy(EXAMPLE)
    chain["publication"]["arxiv"] = 2606.09611
    chain["paper_assessment"]["overall_validity"] = True
    obs = next(s for s in chain["statements"] if s.get("evidence") and s["evidence"][0].get("values"))
    obs["evidence"][0]["values"][0]["value"] = "1.5e3"
    normalize(chain)
    assert chain["publication"]["arxiv"] == "2606.09611"
    assert chain["paper_assessment"]["overall_validity"] == "YES"
    assert obs["evidence"][0]["values"][0]["value"] == 1500.0


def test_dangling_reference_is_reported():
    chain = copy.deepcopy(EXAMPLE)
    chain["relations"][0]["object"] = "wang2026:DOES_NOT_EXIST"
    assert any("DOES_NOT_EXIST" in i for i in validate_chain(chain))


def test_dump_round_trips():
    text = dump_chain(copy.deepcopy(EXAMPLE))
    assert yaml.safe_load(text) == EXAMPLE
    assert "\nrelations:\n  - {id: 'wang2026:R3', subject:" in text  # one flow-style line per relation


def test_cli_writes_yaml_next_to_pdf(pdf, monkeypatch):
    monkeypatch.setattr(convert_mod.anthropic, "Anthropic", lambda: FakeClient(reply(EXAMPLE)))
    assert cli.main([str(pdf), "-q"]) == 0
    out = pdf.with_suffix(".yaml")
    assert validate_chain(yaml.safe_load(out.read_text())) == []


def test_cli_exit_1_when_still_invalid(pdf, tmp_path, monkeypatch):
    bad, _ = broken_chain()
    monkeypatch.setattr(convert_mod.anthropic, "Anthropic", lambda: FakeClient(reply(bad)))
    out = tmp_path / "out.yaml"
    assert cli.main([str(pdf), "-o", str(out), "--max-repairs", "0", "-q"]) == 1
    assert out.is_file()


def test_system_prompt_covers_v04():
    text = convert_mod.system_prompt()[0]["text"]
    assert "derived_checks" in text and "claim_role" in text
    assert validate_chain(yaml.safe_load(data_path("example_v04.yaml").read_text(encoding="utf-8"))) == []


def test_aims_instead_of_hypothesis():
    chain = yaml.safe_load(data_path("example_v06.yaml").read_text(encoding="utf-8"))
    assert not any(s["statement_type"] == "HYPOTHESIS" for s in chain["statements"])
    assert validate_chain(chain) == []


def test_intro_first_keeps_intro_statements(pdf):
    intro = {"statements": [s for s in EXAMPLE["statements"] if s.get("paper_part") == "INTRODUCTION"]}
    reworded = copy.deepcopy(EXAMPLE)
    first = next(s for s in reworded["statements"] if s.get("paper_part") == "INTRODUCTION")
    first["text"] = "Something else."
    client = FakeClient(reply(intro), reply(reworded), reply(EXAMPLE))
    result = convert_pdf(pdf, client=client, intro_first=True)
    assert result.valid and result.attempts == 2
    assert "only its abstract and introduction" in client.requests[0]["messages"][0]["content"][1]["text"]
    assert client.requests[1]["messages"][2]["content"].startswith("Now read the whole paper")
    assert "was reworded" in client.requests[2]["messages"][-1]["content"]
