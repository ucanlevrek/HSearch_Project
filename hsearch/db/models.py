from dataclasses import dataclass


@dataclass
class NodeUsageRow:
    houdini_version: str
    node_context: str
    node_type: str
    node_label: str
    usage_count: int
