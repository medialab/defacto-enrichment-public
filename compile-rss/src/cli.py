import click

from src.combine_files import combine_files
from src.get_history import GitRepo


@click.group()
def cli():
    pass


@cli.command("get-history")
@click.option("--repo", type=click.Path(exists=True))
@click.argument("files", type=click.Path(), nargs=-1)
def get_history(repo, files):
    git_repo = GitRepo(repo)
    git_repo(files)


@cli.command("flatten")
@click.option("-d", "--directory", type=click.Path(dir_okay=True, file_okay=False))
@click.option("-o", "--output", type=click.Path(dir_okay=True, file_okay=False))
def compile(directory, output):
    combine_files(directory, output)


if __name__ == "__main__":
    cli()
