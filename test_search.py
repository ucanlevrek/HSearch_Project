
from hsearch.db.csv_backend import (
    get_usage_counts_by_label,
    increment_usage,
    DEFAULT_DB_PATH,
)
from hsearch.catalog import build_node_catalog, NodeDefinition
from hsearch.core.search_core import SearchItem, search

from typing import List, Dict
import sys
from pathlib import Path

import hou


PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


def main():
    print("building node catalog")
    node_defs = build_node_catalog()

    query = "transform"
    print("searching for {} in SOPS".format(query))

    result = search(
        node_defs=node_defs,
        query=query,
        context_filter="Sop"
    )

    for r in result:
        print(r, "\n")


if __name__ == "__main__":
    main()
