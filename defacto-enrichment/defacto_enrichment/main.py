import json
from argparse import ArgumentParser
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
        json_object: Dict,
        data_dir: Path = DATA_DIR,
    ) -> None:
        """Initially parse and

        Args:
            json_object (Path | None, optional): Path to JSON export of RSS feed. Defaults to None.
            data_dir (Path, optional): Path to directory for enriched CSV files. Defaults to DATA_DIR.
        """

        # Parse JSON export of RSS feed
        self.database_export = json_object
        self.database_export_copy = json_object.copy()
        self.data_items = json_object["data"]

        # Manage file paths
        self.appearance_csv = data_dir.joinpath("appearances.csv")
        self.shared_content_csv = data_dir.joinpath("shared_content.csv")
        self.fact_check_csv = data_dir.joinpath("fact_checks.csv")
        self.new_export_json = data_dir.joinpath("enriched-urls.json")

    def flatten_export(self):
        """Flatten JSON data into 3 CSV files."""

        flatten(
            appearance_file=self.appearance_csv,
            fact_check_file=self.fact_check_csv,
            content_file=self.shared_content_csv,
            data=self.data_items,
        )

    def enrichment(
        self,
        config: str | Dict | None = None,
        with_shared_content_file: bool = True,
        minall_output: Path = MINALL_OUTPUT,
    ):
        """Enrich flattened CSV files with imported Minall app.

        Args:
            config (str | Dict | None, optional): Minet config in YAML file (str), in parsed object (Dict), or in environment variables (None). Defaults to None.
            with_shared_content_file (bool, optional): Whether to attempt colleciton of shared content. Defaults to True.
            minall_output (Path, optional): Directory for enriched CSV files. Defaults to MINALL_OUTPUT.
        """

        # For testing purposes, adjust presence of shared_content file
        if with_shared_content_file:
            shared_content_file = str(self.shared_content_csv)
        else:
            shared_content_file = None

        # ---------- APPEARANCE ENRICHMENT ------------ #
        print(
            "\n",
            Panel(
                f"Appearance metadata input/output:\n\t{self.appearance_csv}\nSharedContent metadata input/output:\n\t{self.shared_content_csv}",
                title="[bold red]Appearances",
                subtitle="[red]Minall data collection",
            ),
        )
        minall = Minall(
            database=None,
            config=config,
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

        # ----------- FACT CHECK ENRICHMENT ----------- #
        print(
            "\n",
            Panel(
                f"Fact-check metadata input/output:\n\t{self.fact_check_csv}",
                title="[bold red]Fact Checks",
                subtitle="[red]Minall data collection",
            ),
        )
        minall = Minall(
            database=None,
            config=config,
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
        """Rebuild JSON from enriched CSV files."""

        rebuild(
            database_export=self.database_export,
            appearances_csv=self.appearance_csv,
            shared_content_csv=self.shared_content_csv,
            fact_check_csv=self.fact_check_csv,
        )
        print(self.new_export_json)
        with open(self.new_export_json, "w") as f:
            json.dump(self.database_export, f, indent=4, ensure_ascii=False)


def parse_input_data() -> Dict:
    parser = ArgumentParser()
    parser.add_argument("--datafile")
    args = parser.parse_args()
    datafile = args.datafile
    if datafile:
        assert Path(datafile).is_file()
    # If provided with a file, parse it
    if datafile:
        with open(datafile, "r") as f:
            database_export = json.load(f)
            if isinstance(database_export, List):
                database_export = {"data": database_export}
    # Otherwise, export the most recent data
    # from the environment variable's endpoint
    else:
        database_export = get_data()
    return database_export


def main():
    # Parse input data
    database_export = parse_input_data()

    # Initialize the app with the data and file paths
    app = App(json_object=database_export)

    # Run the app's 3 steps
    app.flatten_export()
    app.enrichment()
    app.rebuild_export()


if __name__ == "__main__":
    main()
