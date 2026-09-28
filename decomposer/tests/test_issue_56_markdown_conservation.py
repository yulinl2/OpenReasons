"""OpenReasons #56: the two planted cases the Markdown adapter mis-handled at 49f62fb.

1. A hard-wrapped list item loses every line after the first (P1 fired at 0.288/0.388
   on real and planted text; the unwrapped twin of the same item scores 0.917).
2. A colon inside a bolded identifier (``**Gu & Dao, arXiv:2312.00752.**``) is read as
   a ``Key: value`` form field, because ``_METAFIELD`` accepted any capitalised prefix
   before a colon regardless of whether a matching bold-close sat there too.

Both must FAIL against the adapter at commit 49f62fb and PASS once the adapter
conserves continuation lines and requires the metadata-field's closing marker to
match its opening one.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decomposer.adapters import markdown  # noqa: E402
from decomposer.verify.invariants import check_character_coverage  # noqa: E402

WRAPPED_DOC = """\
# Doc

## Section

- **First item** starts on this line and then the sentence keeps
  going on a continuation line that is indented by two spaces, and it
  keeps going for a third line before it finally ends here.
- Second item on one line only.
"""

UNWRAPPED_DOC = """\
# Doc

## Section

- **First item** starts on this line and then the sentence keeps going on a continuation line that is indented by two spaces, and it keeps going for a third line before it finally ends here.
- Second item on one line only.
"""

ARXIV_DOC = """\
# Doc

## Related Work

- **Gu \\& Dao, arXiv:2312.00752.** Selective state-space models are a promising direction.
"""


class _Decomp:
    """Just enough surface for check_character_coverage's all_nodes() call."""

    def __init__(self, root):
        self._root = root

    def all_nodes(self):
        return [self._root, *self._root.iter_descendants()]


def _coverage(doc_text: str) -> float:
    norm = markdown.normalize_text(doc_text)
    root, _edges = markdown.extract(norm.text, "d", "d")
    result = check_character_coverage(_Decomp(root), normalized_len=len(norm.text), min_ratio=0.0)
    return result.metrics["coverage_ratio"]


def test_wrapped_list_item_continuation_conserved():
    """The wrapped item must score close to its unwrapped twin, not lose ~2/3 of itself."""
    wrapped = _coverage(WRAPPED_DOC)
    unwrapped = _coverage(UNWRAPPED_DOC)
    assert wrapped >= 0.9, f"wrapped coverage={wrapped} (49f62fb scored ~0.388)"
    assert unwrapped >= 0.9
    assert abs(wrapped - unwrapped) < 0.05, (
        f"wrapping alone should not move coverage: wrapped={wrapped} unwrapped={unwrapped}"
    )


def test_wrapped_list_item_text_includes_continuation_lines():
    norm = markdown.normalize_text(WRAPPED_DOC)
    root, _edges = markdown.extract(norm.text, "d", "d")
    items = [n for n in root.iter_descendants() if n.type == "list_item"]
    assert len(items) == 2
    first = items[0]
    assert "starts on this line" in first.text
    assert "keeps going for a third line before it finally ends here" in first.text


def test_arxiv_colon_is_not_a_metadata_field():
    norm = markdown.normalize_text(ARXIV_DOC)
    root, _edges = markdown.extract(norm.text, "d", "d")
    nodes = [n for n in root.iter_descendants() if n.type in ("list_item", "metadata_field")]
    assert len(nodes) == 1
    node = nodes[0]
    assert node.type == "list_item", (
        f"'Gu & Dao, arXiv:2312.00752.' misread as metadata_field (key={node.title!r})"
    )
    assert "arXiv:2312.00752" in node.text
