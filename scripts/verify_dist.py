from __future__ import annotations

import re
import sys
import tarfile
import tomllib
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


def fail(message: str) -> None:
    raise SystemExit(message)


def canonicalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def single_artifact(dist_dir: Path, pattern: str) -> Path:
    matches = sorted(dist_dir.glob(pattern))
    if len(matches) != 1:
        fail(f"Expected one {pattern} artifact, found: {matches}")
    return matches[0]


def verify_wheel(wheel: Path, project_name: str, version: str) -> None:
    distribution_dir = f"{project_name.replace('-', '_')}-{version}.dist-info"

    with ZipFile(wheel) as archive:
        names = archive.namelist()
        metadata_path = f"{distribution_dir}/METADATA"
        if metadata_path not in names:
            fail(f"Wheel does not contain {metadata_path}")

        metadata = BytesParser().parsebytes(archive.read(metadata_path))
        expected_fields = {
            "Name": project_name,
            "Version": version,
            "License-Expression": "MIT",
            "Requires-Python": ">=3.12",
        }
        for field, expected in expected_fields.items():
            if metadata[field] != expected:
                fail(f"Unexpected {field}: {metadata[field]!r}, expected {expected!r}")

        allowed_roots = {"oblidog_client", distribution_dir}
        unexpected = sorted(
            name
            for name in names
            if PurePosixPath(name).parts
            and PurePosixPath(name).parts[0] not in allowed_roots
        )
        if unexpected:
            fail(f"Unexpected wheel paths: {unexpected}")
        if not any(name.startswith("oblidog_client/") for name in names):
            fail("Wheel does not contain the oblidog_client package")
        if any("findog_client" in PurePosixPath(name).parts for name in names):
            fail("Wheel contains the legacy findog_client package")


def verify_sdist(sdist: Path, project_name: str, version: str) -> None:
    root = f"{project_name.replace('-', '_')}-{version}"
    expected_package = f"{root}/src/oblidog_client/"
    legacy_package = f"{root}/src/findog_client/"
    sensitive_parts = {".env", ".git", ".venv", "__pycache__"}
    sensitive_suffixes = {".key", ".p12", ".pem", ".pfx"}

    with tarfile.open(sdist) as archive:
        names = archive.getnames()
        if not names or any(PurePosixPath(name).parts[0] != root for name in names):
            fail(f"Source distribution must contain only the {root} root directory")
        if not any(name.startswith(expected_package) for name in names):
            fail("Source distribution does not contain the oblidog_client package")
        if any(name.startswith(legacy_package) for name in names):
            fail("Source distribution contains the legacy findog_client package")

        suspicious = sorted(
            name
            for name in names
            if sensitive_parts.intersection(PurePosixPath(name).parts)
            or PurePosixPath(name).suffix.lower() in sensitive_suffixes
        )
        if suspicious:
            fail(f"Source distribution contains sensitive paths: {suspicious}")


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    dist_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "dist").resolve()
    project = tomllib.loads((project_root / "pyproject.toml").read_text())["project"]
    project_name = canonicalize(project["name"])
    version = project["version"]

    wheel = single_artifact(dist_dir, "*.whl")
    sdist = single_artifact(dist_dir, "*.tar.gz")
    verify_wheel(wheel, project_name, version)
    verify_sdist(sdist, project_name, version)
    print(f"Verified {wheel.name} and {sdist.name}")


if __name__ == "__main__":
    main()
