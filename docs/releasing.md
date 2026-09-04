# Releasing `oblidog-client`

Package releases are built by GitHub Actions and published with PyPI Trusted Publishing. The workflow does not use a PyPI password or long-lived API token.

## One-time configuration

Create two GitHub environments in `oblidog/oblidog-client-python`:

- `pypi` for production releases; configure required reviewers so publication needs explicit approval
- `testpypi` for deliberate dry runs; reviewer protection is recommended

Configure a Trusted Publisher for `oblidog-client` on both PyPI and TestPyPI with these values:

| Setting | Value |
| --- | --- |
| Owner | `oblidog` |
| Repository | `oblidog-client-python` |
| Workflow | `release.yml` |
| Environment | `pypi` on PyPI, `testpypi` on TestPyPI |

PyPI supports a pending Trusted Publisher when the project does not exist yet. This lets the first successful production workflow create the `oblidog-client` project. Do not add `PYPI_TOKEN`, a password, or another publishing secret to GitHub.

## TestPyPI dry run

1. Set the intended package version in `pyproject.toml`, merge it to `main`, and create the matching `vX.Y.Z` tag.
2. Run the **Release** workflow manually.
3. Supply the existing tag and select the only manual target: `testpypi`.
4. Approve the `testpypi` environment deployment if protection is enabled.
5. Install the result from TestPyPI and perform any additional manual checks.

A manual dispatch can never invoke the production publication job. TestPyPI uses a separate job, environment, Trusted Publisher, and hard-coded repository URL.

## Production release

1. Confirm that `pyproject.toml` contains the intended version and all checks on `main` pass.
2. Create or reuse the matching `vX.Y.Z` tag.
3. Publish a GitHub Release for that tag.
4. Review the `pypi` environment deployment and approve it.
5. Verify the release at `https://pypi.org/project/oblidog-client/`.

The workflow rejects malformed tags, tag/project version mismatches, and versions that are not newer than the latest stable version already present on the selected index. A single global concurrency group serializes all package release runs. The build job creates and tests the distributions once; publication jobs download those exact workflow artifacts.
