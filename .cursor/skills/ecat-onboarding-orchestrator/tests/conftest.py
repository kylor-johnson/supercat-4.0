import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

# The check modules are unit-tested by import, while the three validators and the gate
# are tested through their CLI. Both matter: the CLI is the contract an operator uses,
# and a per-check import test is what keeps a failure message specific enough to act on.
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def fixtures():
    return FIXTURES_DIR


@pytest.fixture
def rows_from(tmp_path):
    """Write a CSV and return (rows, lookup) the way every check receives them."""
    from preflight.core import load_rows

    counter = {"n": 0}

    def _load(text, name=None):
        counter["n"] += 1
        path = tmp_path / (name or f"input_{counter['n']}.csv")
        path.write_text(text, encoding="utf-8")
        return load_rows(path)

    return _load


@pytest.fixture
def client_profiles():
    """Every real CLIENT_PROFILE.md, found by walking up to the eCat_Onboarding folder.

    The skill lives inside the workspace it serves, so the depth from here to
    `eCat_Onboarding/` is an accident of layout rather than something to hard-code.
    """
    for parent in Path(__file__).resolve().parents:
        onboarding = parent / "eCat_Onboarding"
        if onboarding.is_dir():
            return sorted(onboarding.glob("*/CLIENT_PROFILE.md"))
    return []


@pytest.fixture
def severities():
    """Collapse findings to a {severity: [message, ...]} dict for assertions."""
    def _by(findings):
        out = {}
        for f in findings:
            out.setdefault(f.severity, []).append(f.render())
        return out
    return _by


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
