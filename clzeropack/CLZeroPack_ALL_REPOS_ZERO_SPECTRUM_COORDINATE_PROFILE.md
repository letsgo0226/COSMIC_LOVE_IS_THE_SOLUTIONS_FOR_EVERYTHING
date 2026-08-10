# CLZeroPack All-Repos Zero-Spectrum Coordinate Profile

`CLZeroPack/AllReposZeroSpectrumCoordinate/1.0` generates one account-level
zero-spectrum coordinate for a repository set.

It defines:

```text
Repo manifest bytes
-> zlib
-> base64 Payload
-> G_all
-> rho_all = 1/2+i*log(1+G_all)
```

## What Is Combined

The lightweight iSH one-liner combines repository metadata:

```text
id
full_name
default_branch
visibility
archived
size
url
```

This is intentionally a metadata snapshot, not a full clone of every file in
every repository.

## Why Metadata First

Fetching every file from every repository is possible but expensive on iSH.
The metadata-level coordinate gives a stable first layer:

```text
all visible repositories
-> canonical sorted manifest
-> account-level coordinate rho_all
```

File-level and commit-tree-level coordinates can be layered later.

## Usage

Install Python once:

```sh
apk add --no-cache python3
```

Generate the public repository coordinate for `letsgo0226`:

```sh
sh CLZeroPack_ALL_REPOS_ZERO_SPECTRUM_COORDINATE_ONE_LINER.sh
```

Specify owner and output:

```sh
sh CLZeroPack_ALL_REPOS_ZERO_SPECTRUM_COORDINATE_ONE_LINER.sh letsgo0226 all_repos_coordinate.json
```

The output contains:

```text
Payload
G_all
rho_all
H_s
Manifest.RepositoryCount
Manifest.Entries
```

## Private Repository Boundary

The iSH one-liner uses GitHub's public API by default. Private repositories are
not included unless a future authenticated variant uses an appropriate token or
GitHub App connector path.

The GitHub connector in ChatGPT may see repositories that the public iSH runtime
cannot see. Therefore the scope must always be recorded in the certificate.

## Boundary

`rho_all` is a coordinate for a repository metadata snapshot. It is not a
cryptographic digest, not a proof of all code contents, and not a full archival
backup of all repositories.
