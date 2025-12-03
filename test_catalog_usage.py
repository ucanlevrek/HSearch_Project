
# test_catalog_and_usage.py
#
# Amaç:
#   1) Houdini'den node katalogunu çek
#   2) Birkaç tanesini yazdır
#   3) CSV usage DB'yi oku, özetini yazdır
#   4) Katalogdaki ilk node için usage arttır ve farkı gör

from hsearch.db.csv_backend import (
    get_usage_counts_by_label,
    increment_usage,
    DEFAULT_DB_PATH,
)
from hsearch.catalog import build_node_catalog, NodeDefinition
from hsearch.core.search_core import search
import sys
from pathlib import Path

import hou  # Houdini içinde çalıştırıyoruz

# ------------------------------------------------------------
# 1) Proje path'ini Python'a tanıt (hsearch paketini bulsun)
# ------------------------------------------------------------

# Bu script'i HSearchBarProject klasörünün içinden çalıştırıyorsan gerek olmayabilir.
# Ama "ImportError: No module named hsearch" görürsen bu kısmı kendine göre düzenle.
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# ------------------------------------------------------------
# 2) Proje modüllerini import et
# ------------------------------------------------------------


def inspect_example_node():
    print("\n=== Inspecting an example hou.Node ===")
    testquery = "agent"
    testcontext = "Object"


def main():
    # --------------------------------------------------------
    # A) Node katalogunu Houdini'den çek
    # --------------------------------------------------------
    print("=== Building node catalog from Houdini ===")
    node_defs = build_node_catalog()
    print(f"Total node definitions: {len(node_defs)}")

    print("\nFirst 10 NodeDefinition entries:")
    for nd in node_defs[:10]:
        # nd: NodeDefinition(node_context, node_type, node_label)
        print(
            f"  context={nd.node_context!r}, type={nd.node_type!r}, label={nd.node_label!r}")

    # --------------------------------------------------------
    # B) hou.Node üzerinden hangi datayı kullandığımızı gör
    # --------------------------------------------------------
    inspect_example_node()

    # --------------------------------------------------------
    # C) Mevcut usage DB özetini yazdır
    # --------------------------------------------------------
    print("\n=== Current usage DB summary ===")
    usage_before = get_usage_counts_by_label()
    print(f"DB file path: {DEFAULT_DB_PATH}")
    print(f"Number of labels in DB: {len(usage_before)}")

    # İlk birkaç label'ı yazdıralım
    for label, count in list(usage_before.items())[:10]:
        print(f"  {label!r}: {count}")

    # --------------------------------------------------------
    # D) Katalogdaki ilk node için usage arttır
    # --------------------------------------------------------
    print("\n=== Simulating a usage increment for the first catalog entry ===")
    if not node_defs:
        print("No node definitions found, nothing to test.")
        return

    sample: NodeDefinition = node_defs[0]
    print("Sample node from catalog:")
    print(
        f"  context={sample.node_context!r}, type={sample.node_type!r}, label={sample.node_label!r}")

    # Burada DB'ye bir "kullanım" ekliyo

    print("\nDone. Now you can open the CSV file manually and inspect its rows if you want.")


if __name__ == "__main__":
    main()
