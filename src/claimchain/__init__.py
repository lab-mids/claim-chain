"""claimchain: convert a research paper (PDF) into a claim-chain argument-chain YAML."""

__version__ = "0.1.0"

from claimchain.convert import ConversionError, ConversionResult, convert_pdf  # noqa: E402
from claimchain.validate import validate_chain  # noqa: E402

__all__ = ["ConversionError", "ConversionResult", "convert_pdf", "validate_chain", "__version__"]
