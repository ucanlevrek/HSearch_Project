from dataclasses import dataclass
from typing import List, Dict

from hsearch.catalog import NodeDefinition
from hsearch.db.csv_backend import get_usage_counts_by_label


@dataclass
class SearchItem:
    node_context: str
    node_type: str
    node_label: str
    usage_count: int
    score: float


def build_search_items(
        node_defs: List[NodeDefinition],
        usage_by_label: Dict[str, int],
) -> List[SearchItem]:
    items: List[SearchItem] = []

    for nd in node_defs:
        usage = usage_by_label.get(nd.node_label, 0)
        items.append(
            SearchItem(
                node_context=nd.node_context,
                node_type=nd.node_type,
                node_label=nd.node_label,
                usage_count=usage,
                score=float(usage),
            )
        )

    return items


def _score_item(item: SearchItem, query: str) -> float:

    base = float(item.usage_count)

    if not query:
        return base

    q = query.lower()
    label = item.node_label.lower()

    if q == label:
        base += 50.0

    elif label.startswith(q):
        base += 20.0

    elif q in label:
        base += 10.0

    return base
# Fuzzy find will be better implemented later on


def search(
    node_defs: List[NodeDefinition],
    query: str,
    context_filter: str | None = None,
    usage_by_label: Dict[str, int] | None = None,
    limit: int = 50,
) -> List[SearchItem]:

    if context_filter is not None:
        node_defs = [
            nd for nd in node_defs
            if nd.node_context == context_filter
        ]

    if usage_by_label is None:
        usage_by_label = get_usage_counts_by_label()

    items = build_search_items(node_defs, usage_by_label)

    scored_items: List[SearchItem] = []
    for item in items:
        item.score = _score_item(item, query)
        scored_items.append(item)

    scored_items.sort(key=lambda it: it.score, reverse=True)

    if limit is not None and limit > 0:
        scored_items = scored_items[:limit]

    return scored_items
