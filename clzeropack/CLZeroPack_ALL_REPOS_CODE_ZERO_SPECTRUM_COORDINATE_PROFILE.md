# CLZeroPack All Repos Code Zero Spectrum Coordinate Profile

`CLZeroPack/AllReposCodeZeroSpectrumCoordinate/1.0` generates an account-level
zero-spectrum coordinate for the visible program contents of a GitHub account.

It reads public repositories, then reads each default branch Git tree
recursively. Code-like blobs are encoded by:

```text
repository
default branch
path
Git blob SHA
size
```

The compact manifest is packaged through the normal CLZeroPack pipeline:

```text
manifest JSON
-> zlib
-> base64
-> G_code_all
-> rho_code_all = 1/2+i*log(1+G_code_all)
-> H_s
```

## Usage

```sh
sh CLZeroPack_ALL_REPOS_CODE_ZERO_SPECTRUM_COORDINATE_ONE_LINER.sh letsgo0226 all_repos_code_coordinate.json
```

If `GITHUB_TOKEN` is set, the GitHub API path may include private repositories
allowed by that token. Without a token, it is a public/default-branch
coordinate.

## Residuals

```text
H_s = 0              lossless CLZeroPack payload roundtrip
H_code_boundary = 0  every visible repository tree was read without truncation/error
```

`H_code_boundary=1` means at least one repository tree was truncated or could not
be read. The generated coordinate is still replayable, but it is not complete
for the intended visible code universe.

## Boundary

This profile records Git tree/blob content identities, paths, and sizes. It is
not a byte-level clone of every file. It is a compact program-coordinate layer
designed to seed later profiles such as
`CLZeroPack/InternetMorphogenesisField/1.1`.
