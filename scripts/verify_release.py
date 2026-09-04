from __future__ import annotations

import json
import re
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

Version = tuple[int, int, int]

TAG_PATTERN = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
INDEXES = {
    "pypi": "https://pypi.org",
    "testpypi": "https://test.pypi.org",
}


def parse_version(value: str) -> Version | None:
    match = re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", value)
    if match is None:
        return None
    return tuple(map(int, match.groups()))


def parse_release_tag(tag: str) -> Version:
    match = TAG_PATTERN.fullmatch(tag)
    if match is None:
        raise SystemExit(f"Release tag must use the exact vX.Y.Z form, got {tag!r}")
    return tuple(map(int, match.groups()))


def published_versions(index_url: str, project_name: str) -> list[Version]:
    url = f"{index_url}/pypi/{project_name}/json"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return []
        raise SystemExit(f"Could not query {url}: HTTP {error.code}") from error
    except (OSError, ValueError) as error:
        raise SystemExit(f"Could not query {url}: {error}") from error

    versions = (parse_version(value) for value in payload.get("releases", {}))
    return sorted(version for version in versions if version is not None)


def verify_release(
    tag: str,
    target: str,
    *,
    project_file: Path,
    existing_versions: list[Version] | None = None,
) -> None:
    if target not in INDEXES:
        raise SystemExit(f"Unknown publication target: {target!r}")

    project = tomllib.loads(project_file.read_text())["project"]
    project_version_text = project["version"]
    project_version = parse_version(project_version_text)
    if project_version is None:
        raise SystemExit(
            f"Project version must use the exact X.Y.Z form, got {project_version_text!r}"
        )

    tag_version = parse_release_tag(tag)
    if tag_version != project_version:
        raise SystemExit(
            f"Tag {tag!r} does not match project version {project_version_text!r}"
        )

    if existing_versions is None:
        existing_versions = published_versions(INDEXES[target], project["name"])
    if existing_versions and project_version <= max(existing_versions):
        latest = ".".join(map(str, max(existing_versions)))
        raise SystemExit(
            f"Version {project_version_text} is not newer than {latest} on {target}"
        )

    print(f"Verified {tag} for {project['name']} {project_version_text} on {target}")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: verify_release.py vX.Y.Z pypi|testpypi")
    project_root = Path(__file__).resolve().parent.parent
    verify_release(
        sys.argv[1],
        sys.argv[2],
        project_file=project_root / "pyproject.toml",
    )


if __name__ == "__main__":
    main()
