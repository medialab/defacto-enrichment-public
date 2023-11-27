from pathlib import Path
from sqlite3 import Connection

from defacto_enrichment.types import Appearance, FactCheck, SharedContent
from src.constants import (
    TEMP_APPEARANCES,
    TEMP_DIR,
    TEMP_FACT_CHECKS,
    TEMP_SHARED_CONTENT,
)
from src.flattener import flattener
from src.table import Table


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
