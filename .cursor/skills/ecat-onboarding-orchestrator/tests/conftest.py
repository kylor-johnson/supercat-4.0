import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def fixtures():
    return FIXTURES_DIR


@pytest.fixture
def run_script():
    """Run a script in scripts/ and return (returncode, combined_output)."""
    def _run(name, *args):
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / name), *args],
            capture_output=True,
            text=True,
        )
        return proc.returncode, proc.stdout + proc.stderr
    return _run


@pytest.fixture
def make_image_dir(tmp_path):
    """Create an image dir; write files of a given byte size on demand."""
    img_dir = tmp_path / "images"
    img_dir.mkdir()

    def _add(name, size_bytes):
        (img_dir / name).write_bytes(b"x" * size_bytes)
        return name

    return img_dir, _add


@pytest.fixture
def write_csv(tmp_path):
    def _write(text, name="products.csv"):
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        return path
    return _write
