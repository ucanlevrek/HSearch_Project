import csv
from pathlib import Path
from collections import Counter
from typing import Iterable, Dict, KeysView, List, Tuple

from .models import NodeUsageRow

DEFAULT_DB_DIR = Path.home() / "Hsearch" / "db"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "node_usage_log.csv"


def ensure_db_dir(path: Path = DEFAULT_DB_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _fieldnames() -> List[str]:

    return [
        "houdini_version",
        "node_context",
        "node_type",
        "node_label",
        "usage_count",
    ]


def load_rows(path: Path = DEFAULT_DB_PATH) -> List[NodeUsageRow]:

    if not path.exists():
        return []

    rows: List[NodeUsageRow] = []

    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                usage = int(r["usage_count"])
            except (ValueError, TypeError):
                usage = 0

            rows.append(
                NodeUsageRow(
                    houdini_version=r["houdini_version"],
                    node_context=r["node_context"],
                    node_type=r["node_type"],
                    node_label=r["node_label"],
                    usage_count=usage,
                )
            )

        return rows


def save_rows(rows: Iterable[NodeUsageRow], path: Path = DEFAULT_DB_PATH) -> None:
    ensure_db_dir(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_fieldnames())
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "houdini_version": row.houdini_version,
                    "node_context": row.node_context,
                    "node_type": row.node_type,
                    "node_label": row.node_label,
                    "usage_count": row.usage_count,
                }
            )


def _row_key(row: NodeUsageRow) -> Tuple[str, str, str]:
    return (
        row.node_context,
        row.node_type,
        row.node_label,
    )


def increment_usage(
    *,
        houdini_version: str,
        node_context: str,
        node_type: str,
        node_label: str,
        delta: int = 1,
        path: Path = DEFAULT_DB_PATH,
) -> None:

    rows = load_rows(path)
    key = (node_context, node_type, node_label)

    found = False
    for row in rows:
        if _row_key(row) == key:
            row.usage_count += delta
            row.houdini_version = houdini_version
            found = True
            break

    if not found:
        rows.append(
            NodeUsageRow(
                houdini_version=houdini_version,
                node_context=node_context,
                node_type=node_type,
                node_label=node_label,
                usage_count=delta,
            )
        )

    save_rows(rows, path)


def get_usage_counts_by_label(path: Path = DEFAULT_DB_PATH) -> Dict[str, int]:
    rows = load_rows(path)
    counter: Counter[str] = Counter()

    for r in rows:
        counter[r.node_label] += r.usage_count

    return dict(counter)
