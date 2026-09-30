"""Packaging consistency (Epic AL): the metadata is a *checked* claim, not decoration.

Every package declares a name, a version, a build backend, and console scripts. This gate parses
all eight ``pyproject.toml`` files and asserts they are mutually consistent AND that every
declared entry point actually resolves to an importable ``module:function`` — so a typo'd or
renamed entry point fails here, not for a user after ``pip install``. (The heavier
build-a-wheel-and-install check runs as the ``package`` CI job / ``make package``.)
"""

import importlib
import pathlib
import sys
import tomllib

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]

# name (as declared) -> monorepo directory. The root meta-package is handled separately.
COMPONENTS = {
    "openpriors-analogy": "analogy",
    "openpriors-concept-graph": "concept_graph",
    "openpriors-decomposer": "decomposer",
    "openpriors-grounding": "grounding",
    "openpriors-matcher": "matcher",
    "openpriors-retrieval": "retrieval",
    "openpriors-graph": "graph",
}


def _load(path: pathlib.Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module", autouse=True)
def _wire_path():
    # put every in-tree src root on sys.path so entry-point modules import
    sys.path.insert(0, str(REPO))
    from openpriors._bootstrap import wire_path
    wire_path()


def _all_pyprojects() -> dict:
    out = {"openpriors": _load(REPO / "pyproject.toml")}
    for name, d in COMPONENTS.items():
        pp = REPO / d / "pyproject.toml"
        assert pp.is_file(), f"{name}: missing {pp.relative_to(REPO)}"
        out[name] = _load(pp)
    return out


def test_every_package_is_packaged():
    # the whole point of Epic AL: no package is left un-declared (graphstore used to have none)
    projects = _all_pyprojects()
    assert set(projects) == {"openpriors", *COMPONENTS}


def test_names_match_declaration():
    projects = _all_pyprojects()
    assert projects["openpriors"]["project"]["name"] == "openpriors"
    for name in COMPONENTS:
        assert projects[name]["project"]["name"] == name


def test_versions_are_consistent():
    from openpriors import __version__
    projects = _all_pyprojects()
    for name, proj in projects.items():
        assert proj["project"]["version"] == __version__, f"{name} version drifts from meta"


def test_packages_tuple_matches_components():
    # openpriors.PACKAGES is the single source of truth used by `version` and the dispatcher
    from openpriors import PACKAGES
    assert set(PACKAGES) == set(COMPONENTS)


def test_every_component_has_a_build_backend_and_src_layout():
    projects = _all_pyprojects()
    for name in COMPONENTS:
        proj = projects[name]
        assert "build-system" in proj and "build-backend" in proj["build-system"]
        assert proj["tool"]["setuptools"]["packages"]["find"]["where"] == ["src"]


def test_root_declares_the_unified_entry_point():
    proj = _all_pyprojects()["openpriors"]
    assert proj["project"]["scripts"]["openpriors"] == "openpriors.cli:main"
    assert proj["tool"]["setuptools"]["packages"] == ["openpriors"]


def test_root_all_extra_lists_exactly_the_components():
    proj = _all_pyprojects()["openpriors"]
    assert set(proj["project"]["optional-dependencies"]["all"]) == set(COMPONENTS)


def test_every_declared_entry_point_resolves():
    # a console script "name = pkg.mod:func" must import and expose a callable func — this is the
    # check that would otherwise only fail for a user running the installed command
    projects = _all_pyprojects()
    checked = 0
    for name, proj in projects.items():
        for script, target in proj["project"].get("scripts", {}).items():
            mod_name, _, func_name = target.partition(":")
            mod = importlib.import_module(mod_name)
            fn = getattr(mod, func_name, None)
            assert callable(fn), f"{name}: entry point {script}={target} does not resolve to a callable"
            checked += 1
    assert checked >= 8      # 1 root + analogy/concept-graph/decompose/grounding/matcher/retrieval + 4 graphstore
