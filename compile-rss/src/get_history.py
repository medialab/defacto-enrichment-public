from pathlib import Path
from typing import Any, Generator

from git import Repo
from git.objects.commit import Commit


class GitRepo:
    def __init__(self, path: Path):
        self.git_repo = Repo(path)
        assert not self.git_repo.bare

    def file_stat(self, commit: Commit) -> Generator[Any, None, None]:
        committed_files = commit.stats.files
        for filename, info in committed_files.items():
            if filename in self.files:
                yield filename, str(commit.committed_datetime), commit.hexsha
                # yield filename, commit.committed_date, str(commit.committed_datetime)

    def __call__(self, files: list):
        self.files = files
        for commit in self.git_repo.iter_commits(all=True, paths=files):
            for info in self.file_stat(commit):
                print(info)
                commit_hex = info[-1]
                print(self.git_repo.refs)
                break
            break
