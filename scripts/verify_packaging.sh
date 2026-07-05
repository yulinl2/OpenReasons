#!/usr/bin/env bash
# Epic AL packaging gate: prove every package actually builds a wheel and the whole thing
# installs + imports + runs from those wheels — so "it's a package" is a checked claim.
#
#   1. build a wheel for each of the 8 packages (root meta + 7 components), no network needed
#   2. install them into a FRESH venv (local wheels via --find-links; third-party deps from PyPI)
#   3. from OUTSIDE the source tree, run `openpriors --help` / `version` and import every package
#
# Usage:  scripts/verify_packaging.sh [--build-only]
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$REPO/dist"
PKGS=(analogy concept_graph decomposer grounding matcher retrieval graph .)

echo "== [1/3] building wheels into $DIST =="
rm -rf "$DIST"; mkdir -p "$DIST"
for p in "${PKGS[@]}"; do
  echo "  -> $p"
  pip wheel --no-deps --no-build-isolation -w "$DIST" "$REPO/$p" >/dev/null
done
n=$(find "$DIST" -maxdepth 1 -name 'openpriors*.whl' | wc -l | tr -d ' ')
echo "  built $n wheels"
[ "$n" -ge 8 ] || { echo "FAIL: expected >= 8 wheels, got $n"; exit 1; }

if [ "${1:-}" = "--build-only" ]; then echo "build-only: OK"; exit 0; fi

echo "== [2/3] fresh-venv install =="
VENV="$(mktemp -d)/venv"
python3 -m venv "$VENV"
# local wheels resolve via --find-links; pydantic/lxml/pylatexenc come from the index
"$VENV/bin/pip" install -q -U pip
"$VENV/bin/pip" install -q --find-links "$DIST" "openpriors[all]"

echo "== [3/3] run from OUTSIDE the source tree (exercises the installed wheels) =="
cd /tmp
"$VENV/bin/openpriors" --help >/dev/null
"$VENV/bin/openpriors" version
"$VENV/bin/python" -c "import openpriors, analogy, concept_graph, matcher, decomposer, grounding, retrieval, graphstore; print('all packages import from wheels: OK')"
echo "PACKAGING OK"
