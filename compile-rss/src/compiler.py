import json
from pathlib import Path
from sqlite3 import Connection
from typing import Dict, List

from defacto_enrichment.flatten import flatten
from defacto_enrichment.types import Appearance, FactCheck, SharedContent

from src.table import Table

TEMP_DIR = Path(__file__).parent.joinpath("tmp")
TEMP_APPEARANCES = TEMP_DIR.joinpath("appearances.csv")
TEMP_FACT_CHECKS = TEMP_DIR.joinpath("fact_checks.csv")
TEMP_SHARED_CONTENT = TEMP_DIR.joinpath("shared_content.csv")
DB = TEMP_DIR.joinpath("sqlite.db")


class Compiler:
    def __init__(self, connection: Connection) -> None:
        TEMP_DIR.mkdir(exist_ok=True)
        self.connection = connection
        self.appearance = Table(
            connection,
            name="appearance",
            fieldnames=Appearance.fieldnames(),
            primary_key=["exact_url"],
        )
        self.fact_check = Table(
            connection,
            name="fact_check",
            fieldnames=FactCheck.fieldnames(),
            primary_key=["exact_url"],
        )
        self.shared_content = Table(
            connection,
            name="shared_content",
            fieldnames=SharedContent.fieldnames(),
            primary_key=["post_url", "content_url"],
        )

        self.n_fact_checks = 0
        self.n_apperances = 0

    def __call__(self, file: Path):
        # Flatten the JSON into 3 CSV files
        flattener(file)
        # Coalesce the data from the 3 CSV files into the 3 SQL tables
        self.appearance.coalesce(infile=TEMP_APPEARANCES)
        self.fact_check.coalesce(infile=TEMP_FACT_CHECKS)
        self.shared_content.coalesce(infile=TEMP_SHARED_CONTENT)

    def export(self, output: str):
        output_dir = Path(output)
        output_dir.mkdir(exist_ok=True)


def flattener(file: Path) -> None:
    with open(file, "r") as f:
        loaded_json = json.load(f)
        if isinstance(loaded_json, List):
            data = loaded_json
        elif isinstance(loaded_json, Dict) and loaded_json.get("data"):
            data = loaded_json["data"]
        else:
            return
        flatten(
            appearance_file=TEMP_APPEARANCES,
            fact_check_file=TEMP_FACT_CHECKS,
            content_file=TEMP_SHARED_CONTENT,
            data=data,
        )
