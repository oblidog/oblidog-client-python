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

The `oblidog-client` project already exists on PyPI, so configure the Trusted
Publisher for that existing project. Do not add `PYPI_TOKEN`, a password, or
another publishing secret to GitHub.

## TestPyPI dry run

1. Set the intended package version in `pyproject.toml`, merge it to `main`, and create the matching `vX.Y.Z` or prerelease `vX.Y.ZrcN` tag.
2. Run the **Release** workflow manually.
3. Supply the existing tag and select the only manual target: `testpypi`.
4. Approve the `testpypi` environment deployment if protection is enabled.
5. Install the result from TestPyPI and perform any additional manual checks.

A manual dispatch can never invoke the production publication job. TestPyPI uses a separate job, environment, Trusted Publisher, and hard-coded repository URL. Index versions are immutable: if a broken version has already reached TestPyPI, use a higher version such as `0.1.1rc1`; it cannot be replaced or followed by the lower `0.1.0rc1`.

## Production release

1. Merge releasable Conventional Commits to `main`. The **Prepare release** workflow creates a `release/vX.Y.Z` pull request with the version bump and updated `CHANGELOG.md`.
2. Review and merge that pull request after its checks pass. The workflow creates the matching `vX.Y.Z` tag on `main` and a draft GitHub Release containing that version's changelog section.
3. Review and publish the draft GitHub Release.
4. Review the `pypi` environment deployment and approve it.
5. Verify the release at `https://pypi.org/project/oblidog-client/`.

Publishing the draft is the explicit production trigger; creating the draft does not publish the package. The workflow accepts canonical PEP 440 stable versions and release candidates (`X.Y.Z` and `X.Y.ZrcN`). It rejects malformed tags, tag/project version mismatches, and versions that are not newer than the latest version already present on the selected index. A single global concurrency group serializes all package release runs. The build job creates and tests the distributions once; publication jobs download those exact workflow artifacts.
