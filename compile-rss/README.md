# Install

Activate a virtual environment with Python version 3.11 and install the CLI.

```console
$ pip install git+https://github.com/medialab/defacto-enrichment-public.git#subdirectory=compile-rss
```

# Save committed versions of data

Use the command `git-history` to save committed versions of prior URL enrichments to a folder, where each version is written to a file whose name is composed of (a) the date of the commit and (b) the commit's ID.

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
