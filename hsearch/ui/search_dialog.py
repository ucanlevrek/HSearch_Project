from hsearch.catalog import NodeDefinition
from PySide6 import QtWidgets, QtCore

from hou import Node
from typing import List


class NodeSearchDialog(QtWidgets.QDialog):

    def __init__(self, node_def: List[NodeDefinition], parent=None):
        super().__init__(parent)

        self.setWindowTitle("HSearch - Node Browser (prototype)")
