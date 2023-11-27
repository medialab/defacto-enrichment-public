import json
import shutil
from datetime import datetime
from pathlib import Path

import click
from src.combine_files import combine_files
from src.get_history import GitRepo


@click.group()
def cli():
    pass


@cli.command("get-history")
@click.option(
    "--output",
    type=click.Path(dir_okay=True, file_okay=False),
    help="Path to the directory in which to write all the target files' committed versions.",
)
@click.option(
    "--repo",
    type=click.Path(exists=True),
    help="Path to the root of the targeted git repository.",
)
@click.option(
    "--relative-file-name",
    type=click.Path(),
    multiple=True,
    help="Target file's path relative to the git repository.",
)
def get_history(output, repo, relative_file_name):
    git_repo = GitRepo(repo)
    outdir = Path(output)
    outdir.mkdir(exist_ok=True, parents=True)
    for output_stem, data in git_repo.retrieve_files(relative_file_name):
        outfile = outdir.joinpath(output_stem)
        with open(outfile, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


@cli.command("add")
@click.option(
    "--output",
    type=click.Path(dir_okay=True, file_okay=False),
    help="Path to the directory in which to write all the target files' committed versions.",
)
@click.argument("file", type=click.Path(dir_okay=False, file_okay=True))
def add_file_to_history(output, file):
    outdir = Path(output)
    outdir.mkdir(exist_ok=True, parents=True)
    fp = Path(file)
    new_file_name = (
        str(datetime.fromtimestamp(fp.stat().st_mtime).date())
        + "_"
        + fp.stem
        + "".join(fp.suffixes)
    )
    outfile = outdir.joinpath(new_file_name)
    shutil.copy(src=file, dst=str(outfile))


@cli.command("flatten")
@click.option("-d", "--directory", type=click.Path(dir_okay=True, file_okay=False))
@click.option("-o", "--output", type=click.Path(dir_okay=True, file_okay=False))
def compile(directory, output):
    combine_files(directory, output)


if __name__ == "__main__":
    cli()
