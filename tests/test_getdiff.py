from pathlib import Path
import pytest
from gendiff.scripts.generate_diff import generate_diff


FIXTURES_DIR = Path("tests/fixtures")


def build_test_case(file1, file2):
	with open(FIXTURES_DIR / f"diff_{file1}_{file2}.txt") as file:
		diff = file.read().strip()

		return (FIXTURES_DIR / f"{file1}.json", FIXTURES_DIR / f"{file2}.json", diff)


cases = [build_test_case(f1, f2) for f1, f2 in [["file1", "file2"]]]


@pytest.mark.parametrize("path1, path2, expected", cases)
def test_gendiff(path1, path2, expected):
    result = generate_diff(path1, path2)
    assert result == expected
