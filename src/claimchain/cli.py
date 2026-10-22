"""Command line interface: claimchain paper.pdf [-o paper.yaml]."""
import argparse
import sys
from pathlib import Path

import anthropic

from claimchain import __version__
from claimchain.convert import DEFAULT_EFFORT, DEFAULT_MODEL, ConversionError, convert_pdf


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="claimchain",
        description="Convert a research paper (PDF) into a claim-chain argument-chain YAML.",
        epilog="Credentials are read from ANTHROPIC_API_KEY (or another Anthropic SDK credential source). "
               "Exit status: 0 valid YAML written, 1 YAML written but still failing validation, 2 error.",
    )
    p.add_argument("pdf", type=Path, help="input PDF file")
    p.add_argument("-o", "--output", type=Path,
                   help="output YAML file (default: the PDF's path with a .yaml suffix)")
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"Claude model id (default: {DEFAULT_MODEL})")
    p.add_argument("--effort", default=DEFAULT_EFFORT, choices=["low", "medium", "high", "xhigh", "max"],
                   help=f"reasoning effort (default: {DEFAULT_EFFORT})")
    p.add_argument("--max-repairs", type=int, default=2,
                   help="correction rounds when the YAML fails validation (default: 2)")
    p.add_argument("--no-fallback", action="store_true",
                   help="disable the server-side refusal fallback (needed on Bedrock, Vertex AI, Foundry)")
    p.add_argument("--intro-first", action="store_true",
                   help="first fix background, gaps, hypothesis and aims from the abstract and introduction only, "
                        "then encode the whole paper against them (one extra request)")
    p.add_argument("-q", "--quiet", action="store_true", help="no progress messages")
    p.add_argument("--version", action="version", version=f"claimchain {__version__}")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.pdf.is_file():
        print(f"claimchain: {args.pdf} not found", file=sys.stderr)
        return 2
    output = args.output or args.pdf.with_suffix(".yaml")
    log = (lambda m: None) if args.quiet else (lambda m: print(m, file=sys.stderr))

    try:
        result = convert_pdf(args.pdf, model=args.model, effort=args.effort,
                             max_repairs=args.max_repairs, fallback=not args.no_fallback,
                             intro_first=args.intro_first, log=log)
    except (ConversionError, anthropic.APIError) as exc:
        print(f"claimchain: {exc}", file=sys.stderr)
        return 2

    output.write_text(result.yaml_text, encoding="utf-8")
    u = result.usage
    log(f"wrote {output} after {result.attempts} request(s); tokens in {u['input_tokens']} "
        f"(cached {u['cache_read_input_tokens']}), out {u['output_tokens']}")
    if result.issues:
        print(f"claimchain: {output} still has {len(result.issues)} validation problem(s):", file=sys.stderr)
        for issue in result.issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
