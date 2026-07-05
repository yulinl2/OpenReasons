"""The unified ``openpriors`` CLI + the demonstration (Epic AL).

Covers the dispatcher's contract (help / version / unknown verb / forwarding) and the
demonstration's three guarantees: it recomputes live, it is deterministic, and the committed
DEMONSTRATION.md is not stale.
"""

import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from openpriors import __version__, cli, demonstrate  # noqa: E402
from openpriors._bootstrap import wire_path  # noqa: E402

wire_path()


# --- dispatcher contract ---------------------------------------------------------------------
def test_help_lists_every_verb(capsys):
    rc = cli.main(["--help"])
    out = capsys.readouterr().out
    assert rc == 0
    for verb in cli.VERBS:
        assert verb in out


def test_no_args_shows_usage(capsys):
    assert cli.main([]) == 0
    assert "usage: openpriors" in capsys.readouterr().out


def test_unknown_verb_is_rc_2(capsys):
    assert cli.main(["frobnicate"]) == 2
    assert "unknown verb" in capsys.readouterr().err


def test_bootstrap_pins_reproducible_epoch():
    # `openpriors run` regenerates timestamped artifacts; the CLI must pin SOURCE_DATE_EPOCH the
    # same way the Makefile does, or those artifacts churn on the wall clock and drift silently.
    import os
    assert os.environ.get("SOURCE_DATE_EPOCH") == "1735689600"


def test_version_lists_all_packages(capsys):
    from openpriors import PACKAGES
    assert cli.main(["version"]) == 0
    out = capsys.readouterr().out
    assert __version__ in out
    for name in PACKAGES:
        assert name in out


# --- demonstration ---------------------------------------------------------------------------
def test_demonstration_recomputes_and_is_deterministic():
    d1 = demonstrate.build_demonstration(REPO)
    d2 = demonstrate.build_demonstration(REPO)
    assert demonstrate.render_markdown(d1) == demonstrate.render_markdown(d2)
    # it genuinely ran the arc: results ingested, analogies found, conjectures judged, loop closed
    assert d1["n_results"] > 0 and d1["n_analogies"] > 0 and d1["n_conjectures"] > 0
    assert d1["ledger"]["summary"]["confirmed_by_real_paper"] >= 1


def test_committed_demonstration_is_not_stale():
    md = demonstrate.render_markdown(demonstrate.build_demonstration(REPO))
    committed = (REPO / "DEMONSTRATION.md").read_text(encoding="utf-8")
    assert committed == md, "DEMONSTRATION.md is stale — run `openpriors demonstrate`"


def test_demonstrate_check_flag_passes_on_fresh_artifact(capsys):
    assert demonstrate.main(["--check"]) == 0


def test_demonstrate_check_flag_fails_when_stale(tmp_path, capsys):
    stale = tmp_path / "DEMONSTRATION.md"
    stale.write_text("clearly not the real transcript\n", encoding="utf-8")
    assert demonstrate.main(["--check", "--out", str(stale)]) == 1


def test_demonstration_narrates_the_seven_stages():
    md = demonstrate.render_markdown(demonstrate.build_demonstration(REPO))
    for heading in ("Ingest", "Novelty", "Lineage", "Analogy", "Conjecture", "Evaluate", "Confirm"):
        assert heading in md
