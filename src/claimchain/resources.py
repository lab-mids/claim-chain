"""Locate the files shipped with the package (prompts, schema, reference examples)."""
from importlib import resources
from pathlib import Path

# Installed wheels carry the schema and example under claimchain/data (see the
# force-include section of pyproject.toml). In an editable install or a plain
# checkout they are read from their place in the repository instead.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_REPO_FILES = {
    "claim_chain.yaml": _REPO_ROOT / "schema" / "claim_chain.yaml",
    "example.yaml": _REPO_ROOT / "examples" / "wang2026_lattice_genome" / "wang2026_lattice_genome.yaml",
    "example_v04.yaml": _REPO_ROOT / "examples" / "zhuang2017_d019_mgal" / "zhuang2017_d019_mgal_claimchain.yaml",
}


def data_path(name: str) -> Path:
    packaged = resources.files("claimchain") / "data" / name
    if packaged.is_file():
        return Path(str(packaged))
    if name in _REPO_FILES and _REPO_FILES[name].is_file():
        return _REPO_FILES[name]
    raise FileNotFoundError(f"claimchain data file {name!r} not found")


def schema_path() -> Path:
    return data_path("claim_chain.yaml")


def read_prompt(name: str) -> str:
    return (resources.files("claimchain") / "prompts" / name).read_text(encoding="utf-8")
