import pytest
from pathlib import Path
from gendiff.generate_diff import generate_diff


FIXTURES_DIR = Path("tests/fixtures")


def build_test_case(file1, file2, format):
	file1_name = Path(file1).stem
	file2_name = Path(file2).stem

	with open(FIXTURES_DIR / f"diff_{file1_name}_{file2_name}_{format}.txt") as file:
		diff = file.read().strip()

		return (FIXTURES_DIR / f"{file1}", FIXTURES_DIR / f"{file2}", format, diff)


cases = [
	build_test_case(f1, f2, format) for f1, f2, format in [
		["file1.json", "file2.json", "stylish"],
		["file3.yml", "file4.yml", "stylish"],
		["file1.json", "file2.json", "plain"],
		["file3.yml", "file4.yml", "plain"],
		["file1.json", "file2.json", "json"],
		["file3.yml", "file4.yml", "json"],
	]
]


@pytest.mark.parametrize("path1, path2, format, expected", cases)
def test_gendiff(path1, path2, format, expected):
    result = generate_diff(path1, path2, format)
    assert result == expected
