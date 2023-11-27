from pathlib import Path

TEMP_DIR = Path(__file__).parent.joinpath("tmp")
TEMP_DIR.mkdir(exist_ok=True)

TEMP_APPEARANCES = TEMP_DIR.joinpath("appearances.csv")
TEMP_FACT_CHECKS = TEMP_DIR.joinpath("fact_checks.csv")
TEMP_SHARED_CONTENT = TEMP_DIR.joinpath("shared_content.csv")
