import pytest
from pathlib import Path
from gendiff.scripts.generate_diff import generate_diff


FIXTURES_DIR = Path("tests/fixtures")


def build_test_case(file1, file2):
	file1_name = Path(file1).stem
	file2_name = Path(file2).stem

	with open(FIXTURES_DIR / f"diff_{file1_name}_{file2_name}.txt") as file:
		diff = file.read().strip()

		return (FIXTURES_DIR / f"{file1}", FIXTURES_DIR / f"{file2}", diff)


cases = [
	build_test_case(f1, f2) for f1, f2 in [
		["file1.json", "file2.json"],
		["file3.yml", "file4.yml"]
	]
]


@pytest.mark.parametrize("path1, path2, expected", cases)
def test_gendiff(path1, path2, expected):
    result = generate_diff(path1, path2)
    assert result == expected
