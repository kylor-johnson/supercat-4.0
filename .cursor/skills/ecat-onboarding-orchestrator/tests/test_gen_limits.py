"""Guard the generated limit table against drift.

`limits_generated.py` is committed so the gate runs without a checkout of
supercat_server. That convenience is also the risk: a limit changed upstream would leave
the table quietly stale, which is the same class of bug as transcribing it by hand.

`gen_limits.py --check` re-derives the table and diffs it against the committed file, so
drift shows up here rather than in a client's rejected import. It skips when the server
tree is absent, because most runs of this suite happen without it.
"""
import subprocess
import sys
from pathlib import Path

import pytest

from preflight import limits_generated as gen

SERVER_ROOT = Path("~/supercat-code/supercat_server").expanduser()
SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def test_generated_table_records_its_provenance():
    """Without a commit and per-file hashes, "generated" is an unverifiable claim."""
    assert gen.SOURCE_GIT_SHA
    assert gen.GENERATED_AT
    assert gen.SOURCE_FILES
    for path, digest in gen.SOURCE_FILES.items():
        assert path.endswith(".rb"), path
        assert len(digest) >= 8, path


def test_the_models_the_limits_come_from_are_all_parsed():
    models = {meta["model"] for headers in gen.LIMITS.values()
              for meta in headers.values()}
    assert {"Product", "Customer", "ShippingLocation", "Option",
            "OptionGroup"} <= models


@pytest.mark.skipif(not SERVER_ROOT.exists(),
                    reason="supercat_server checkout not present")
def test_committed_table_matches_the_source_tree():
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "tools" / "gen_limits.py"), "--check",
         "--server-root", str(SERVER_ROOT)],
        capture_output=True, text=True)
    assert proc.returncode == 0, (
        "preflight/limits_generated.py is stale — re-run "
        f"tools/gen_limits.py.\n{proc.stdout}{proc.stderr}")
