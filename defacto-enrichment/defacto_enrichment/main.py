import json
from pathlib import Path
from typing import Dict, List

from defacto_enrichment.constants import DATA_DIR, MINALL_OUTPUT
from defacto_enrichment.flatten import flatten
from defacto_enrichment.get_data import get_data
from defacto_enrichment.rebuild import rebuild
from minall.main import Minall
from rich import print
from rich.panel import Panel


class App:
    def __init__(
        self,
        config: str | None = None,
        data_dir: Path = DATA_DIR,
        database_export_file: Path | None = None,
    ) -> None:
        self.config = config
        # Export new data from the database
        if not database_export_file:
            database_export = get_data()
            self.database_export_copy = database_export.copy()
            self.database_export = database_export
            self.data_items = database_export["data"]
        else:
            with open(database_export_file, "r") as f:
                database_export = json.load(f)
                if isinstance(database_export, List):
                    self.data_items = database_export
                    self.database_export_copy = {"data": database_export}
                    self.database_export = self.database_export_copy
                elif isinstance(database_export, Dict) and database_export.get("data"):
                    self.database_export_copy = database_export.copy()
                    self.database_export = self.database_export_copy
                    self.data_items = database_export["data"]

        # Manage file paths
        self.appearance_csv = data_dir.joinpath("appearances.csv")
        self.shared_content_csv = data_dir.joinpath("shared_content.csv")
        self.fact_check_csv = data_dir.joinpath("fact_checks.csv")
        self.new_export_json = data_dir.joinpath("enriched-urls.json")

    def flatten_export(self):
        flatten(
            appearance_file=self.appearance_csv,
            fact_check_file=self.fact_check_csv,
            content_file=self.shared_content_csv,
            data=self.data_items,
        )

    def enrichment(
        self, with_shared_content_file: bool = True, minall_output: Path = MINALL_OUTPUT
    ):
        # For testing purposes, adjust presence of shared_content file
        if with_shared_content_file:
            shared_content_file = str(self.shared_content_csv)
        else:
            shared_content_file = None

        print(
            "\n",
            Panel(
                f"Appearance metadata input/output:\n\t{self.appearance_csv}\nSharedContent metadata input/output:\n\t{self.shared_content_csv}",
                title="[bold red]Appearances",
                subtitle="[red]Minall data collection",
            ),
        )
        # Appearances & shared content
        minall = Minall(
            database=None,
            config=self.config,
            output_dir=str(minall_output),
            links_file=str(self.appearance_csv),
            url_col="clean_url",
            shared_content_file=shared_content_file,
            buzzsumo_only=False,
        )
        minall.collect_and_coalesce()
        minall.export()
        minall_output.joinpath("links.csv").rename(self.appearance_csv)
        minall_output.joinpath("shared_content.csv").rename(self.shared_content_csv)

        print(
            "\n",
            Panel(
                f"Fact-check metadata input/output:\n\t{self.fact_check_csv}",
                title="[bold red]Fact Checks",
                subtitle="[red]Minall data collection",
            ),
        )
        # Fact checks
        minall = Minall(
            database=None,
            config=self.config,
            output_dir=str(minall_output),
            links_file=str(self.fact_check_csv),
            url_col="clean_url",
            shared_content_file=None,
            buzzsumo_only=True,
        )
        minall.collect_and_coalesce()
        minall.export()
        minall_output.joinpath("links.csv").rename(self.fact_check_csv)

    def rebuild_export(self):
        rebuild(
            database_export=self.database_export,
            appearances_csv=self.appearance_csv,
            shared_content_csv=self.shared_content_csv,
            fact_check_csv=self.fact_check_csv,
        )
        print(self.new_export_json)
        with open(self.new_export_json, "w") as f:
            json.dump(self.database_export, f, indent=4, ensure_ascii=False)


def main():
    app = App()
    app.flatten_export()
    app.enrichment()
    app.rebuild_export()


if __name__ == "__main__":
    main()
