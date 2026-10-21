"""Keep copyable documentation examples syntactically valid without API access."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def python_examples() -> list[tuple[str, str]]:
    examples = []
    for path in [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]:
        for index, match in enumerate(
            re.finditer(
                r"^```python\n(.*?)^```\s*$", path.read_text(), re.MULTILINE | re.DOTALL
            ),
            start=1,
        ):
            examples.append((f"{path.relative_to(ROOT)}:example-{index}", match[1]))
    if not examples:
        raise AssertionError("No Python documentation examples found")
    return examples


@pytest.mark.parametrize("name,source", python_examples())
def test_documentation_example_compiles(name: str, source: str) -> None:
    compile(source, name, "exec")
