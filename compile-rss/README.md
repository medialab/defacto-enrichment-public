# `defcomp` De Facto enrichment compiler

This tool is designed to solve a problem. One goal of the `defacto-enrichment` workflow is, thanks to an in-memory SQL database, to retain previous enrichments even when a URL has been deleted or metadata is otherwise no longer available. For this reason, a later iteration of an enrichment might contain less information than a previous iteration.

When you run the `defacto-enrichment` workflow on a set of claim-reviews, you generate a file, `./data/enriched-urls.json'. When that set of claim-reviews is updated regularly and you run the `defacto-enrichment` workflow regularly, you generate a set of files. Ideally, the updated set of claim-reviews would have the previous run's enrichments in them, but this is not always possible. For example, when you're collecting a set of claim-reviews from a source that you cannot modify, you have to save the iterations of the enrichment.

Thus the problem to solve is compiling a set of enrichments, generated over time, retaining all information that was ever available and recorded in an out-file.

---

# Table of contents

- [Install](#install)
- [Gather historic versions of dataset](#gather-historic-versions-of-data)
  - [Git commits](#save-versions-committed-to-git-repository)
  - [Stand-alone file](#add-single-version-of-data-to-compiled-directory)

# Install

Activate a virtual environment with Python version 3.11 and install the CLI.

```console
$ pip install git+https://github.com/medialab/defacto-enrichment-public.git#subdirectory=compile-rss
```

# Gather historic versions of data

## Save versions committed to Git repository

Use the command `git-history` to iterate through all versions of a file committed to a git repository and save them inside a folder. Each version is written to a file whose name is composed of (a) the date of the commit and (b) the commit's ID.

```console
Usage: defcomp get-history [OPTIONS]

Options:
  --output DIRECTORY         Path to the directory in which to write all the
                             target files' committed versions.
  --repo PATH                Path to the root of the targeted git repository.
  --relative-file-name PATH  Target file's path relative to the git
                             repository.
  --help                     Show this message and exit.
```

### Example

Let's say you want to save the committed versions of a file, such as the `enriched-urls.json` file that `defacto-enrichment` generates. The versions were committed in a git repository outside your current working directory (CWD). See the example architecture below.

```console
.
|___git-repo/
    |___main.py
    |___data/
        |___enriched-urls.jon
|___compile-history/ (CWD)
    |___committed-data/
```

To save all the committed versions of `enriched-urls.json` in this example scenario, assign the following information to the `get-history` options:

- `--output` : `./versions`
- `--repo` : `../git-repo`
- `--relative-file-name` : `data/enriched-urls.json`

```console
$ defcomp get-history --output ./versions --repo ../git-repo --relative-file-name data/enriched-urls.json
```

```console
.
|___git-repo/
    |___main.py
    |___data/
        |___enriched-urls.jon
|___compile-history/ (CWD)
    |___committed-data/
        |___2023-05-08_0943ad63bdf7766045d8c2b811cd945923feb2ee.json
        |___2023-05-09_562034382306237e3ea477e7af92fa38abbccb86.json
        |___2023-05-10_8c127f5aade58665b43e289cabf40e5c17202b64.json
```

## Add single version of data to compiled directory

To manually add a single file to a directory of compiled data versions, use the command `defcomp add --output DIRECTORY FILE`.

```console
Usage: defcomp add [OPTIONS] FILE

Options:
  --output DIRECTORY  Path to the directory in which to write all the target
                      files' committed versions.
  --help              Show this message and exit.
```

### Example

Let's say you have a file you generated with the `defacto-enrichment` workflow, `enriched-urls.json`, and you want to add that to a directory you're curating of historic versions of your dataset's enrichment, `./committed-data`.

```console
.
|___data/
    |___enriched-urls.jon
|___compile-history/ (CWD)
    |___committed-data/
```

To add the file to the directory with the same naming convention as used in the command `defcomp get-history`, run the following command:

```console
$ defcomp add --output ./committed-data ../data/enriched-urls.json
```

```console
.
|___data/
    |___enriched-urls.jon
|___compile-history/ (CWD)
    |___committed-data/
        |___2023-11-04_enriched-urls.json
```
