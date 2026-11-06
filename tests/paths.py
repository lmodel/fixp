"""Where the tests find the repository's files, in one place."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "src" / "fixp" / "schema"
SCHEMA = SCHEMA_DIR / "fixp.yaml"
UPSTREAM = ROOT / "upstream"
SPEC = UPSTREAM / "fixp-specification"
RESOURCES = SPEC / "v1-0-STANDARD" / "resources"
SBE_SCHEMA = RESOURCES / "SBEschemaForFIXP.xml"
REPOSITORY = RESOURCES / "FixRepositoryForFIXP.xml"
ORCHESTRA = RESOURCES / "OrchestraForFIXP.xml"
DATA = ROOT / "tests" / "data"
