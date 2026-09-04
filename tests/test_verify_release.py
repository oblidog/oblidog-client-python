from pathlib import Path

import pytest

from scripts.verify_release import parse_release_tag, verify_release


def project_file(tmp_path: Path, version: str = "0.1.0") -> Path:
    path = tmp_path / "pyproject.toml"
    path.write_text(f'[project]\nname = "oblidog-client"\nversion = "{version}"\n')
    return path


def test_release_tag_matches_new_project_version(tmp_path: Path) -> None:
    verify_release(
        "v0.1.0",
        "pypi",
        project_file=project_file(tmp_path),
        existing_versions=[],
    )


def test_release_tag_must_match_project_version(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="does not match"):
        verify_release(
            "v0.2.0",
            "pypi",
            project_file=project_file(tmp_path),
            existing_versions=[],
        )


@pytest.mark.parametrize("tag", ["0.1.0", "v0.1", "v01.1.0", "v0.1.0-rc1"])
def test_release_tag_requires_exact_stable_semver(tag: str) -> None:
    with pytest.raises(SystemExit, match="exact vX.Y.Z"):
        parse_release_tag(tag)


def test_release_version_must_be_newer_than_index(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="is not newer"):
        verify_release(
            "v0.1.0",
            "pypi",
            project_file=project_file(tmp_path),
            existing_versions=[(0, 1, 0)],
        )


def test_manual_target_cannot_be_changed_to_production(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="Unknown publication target"):
        verify_release(
            "v0.1.0",
            "production",
            project_file=project_file(tmp_path),
            existing_versions=[],
        )
