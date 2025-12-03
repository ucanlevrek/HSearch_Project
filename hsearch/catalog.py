from dataclasses import dataclass
from typing import List
import hou


@dataclass
class NodeDefinition:
    node_context: str
    node_type: str
    node_label: str


def build_node_catalog() -> List[NodeDefinition]:
    defs: List[NodeDefinition] = []

    categories = hou.nodeTypeCategories()

    wanted_contexts = ["Objects", "Sop"]

    for cat_key in wanted_contexts:
        cat = categories.get(cat_key)
        if cat is None:
            continue

        for node_type in cat.nodeTypes().values():
            label = node_type.description()
            type_name = node_type.name()

            context_key = cat.name()

            defs.append(
                NodeDefinition(
                    node_context=context_key,
                    node_type=type_name,
                    node_label=label,
                )
            )

    return defs
