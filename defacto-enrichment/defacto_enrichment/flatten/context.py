import csv
from pathlib import Path

from defacto_enrichment.types import Appearance, FactCheck, SharedContent
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)


class Writers:
    def __init__(
        self, appearances_file: Path, shared_content_file: Path, fact_check_file: Path
    ) -> None:
        self.appearances_file = appearances_file
        self.shared_content_file = shared_content_file
        self.fact_check_file = fact_check_file

    def __enter__(self):
        # Set up appearances CSV file
        self.appearances_file_obj = open(self.appearances_file, mode="w")
        self.appearances_file_writer = csv.DictWriter(
            self.appearances_file_obj, Appearance.fieldnames()
        )
        self.appearances_file_writer.writeheader()

        # Set up reviews CSV file
        self.fact_check_file_obj = open(self.fact_check_file, mode="w")
        self.fact_check_file_writer = csv.DictWriter(
            self.fact_check_file_obj, FactCheck.fieldnames()
        )
        self.fact_check_file_writer.writeheader()

        # Set up shared_content CSV file
        self.shared_content_file_obj = open(self.shared_content_file, mode="w")
        self.shared_content_file_writer = csv.DictWriter(
            self.shared_content_file_obj, SharedContent.fieldnames()
        )
        self.shared_content_file_writer.writeheader()

        # Set up progress bar
        self.progress_bar = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        )
        self.progress_bar.start()

        return (
            self.appearances_file_writer,
            self.shared_content_file_writer,
            self.fact_check_file_writer,
            self.progress_bar,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.appearances_file_obj:
            self.appearances_file_obj.close()
        if self.shared_content_file_obj:
            self.shared_content_file_obj.close()
        if self.fact_check_file_obj:
            self.fact_check_file_obj.close()
        self.progress_bar.stop()
