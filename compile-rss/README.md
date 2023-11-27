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

In a subdirectory, `./committed-data`, you want to save the committed versions of prior enrichments. The old enrichments were committed in a git repository, `git-repo/`, outside the current working directory (CWD). See the example architecture below.

```console
.
|___git-repo/
    |___main.py
    |___data/
        |___enriched-urls.jon
|___compile-history/ (CWD)
    |___committed-data/
```

To run the command for the example scenario, input the following information for the options.

- `--output` : `./versions`
- `--repo` : `../git-repo`
- `--relative-file-name` : `data/enriched-urls.json`

```console
$ defcomp get-history --output ./versions --repo ../git-repo --relative-file-name data/enriched-urls.json
```
