from pathlib import Path
from typing import Any, Generator

from git import Repo
from git.objects.commit import Commit
from rich.progress import track


class GitRepo:
    def __init__(self, root_path: str):
        self.repo_path = Path(root_path).absolute()
        if not self.repo_path.is_dir():
            raise NotADirectoryError
        self.git_repo = Repo(self.repo_path)
        self.head = self.git_repo.refs[0]
        assert not self.git_repo.bare

    def file_stat(self, commit: Commit) -> Generator[Any, None, None]:
        committed_files = commit.stats.files
        for filename, _ in committed_files.items():
            if filename in self.targeted_files:
                yield filename, str(commit.committed_datetime), commit.hexsha

    def retrieve_files(self, file_names: list):
        self.targeted_files = file_names
        total_commits = len(
            list(self.git_repo.iter_commits(all=True, paths=file_names))
        )
        for commit in track(
            self.git_repo.iter_commits(all=True, paths=file_names),
            total=total_commits,
            description="Commits...",
        ):
            for info in self.file_stat(commit):
                relative_file_path = info[0]
                extension = Path(relative_file_path).suffix
                commit_hex = info[2]
                commit_date = info[1]
                output_stem = f"{commit_date[:10]}_{commit_hex}{extension}"
                yield output_stem, self.git_repo.git.execute(
                    [
                        "git",
                        "cat-file",
                        "-p",
                        f"{commit_hex}:{relative_file_path}",
                    ]
                )
