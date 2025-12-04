from hsearch.catalog import NodeDefinition
from PySide6 import QtWidgets, QtCore

from hou import Node
from typing import List


class NodeSearchDialog(QtWidgets.QDialog):

    def __init__(
        self,
        node_defs: List[NodeDefinition],
        parent=None,
        result_limit: int = 30,
        visible_rows=10,
    ):
        super().__init__(parent)

        self._all_nodes = node_defs
        self._result_limit = result_limit
        self._visible_rows = visible_rows

        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setModal(False)
        self.setObjectName("HSearchPopup")

        self._build_ui()
        self._update_list("")

    def _build_ui(self):
        print("building ui")
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)

        self.search_edit = QtWidgets.QLineEdit(self)
        self.search_edit.setPlaceholderText("Search nodes...")
        self.search_edit.setFrame(False)

        # Might add a stylesheet
        main_layout.addWidget(self.search_edit)

        self.list_widget = QtWidgets.QListWidget(self)

        self.list_widget.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerItem
        )

        self.list_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )

        self.list_widget.setUniformItemSizes(True)
        main_layout.addWidget(self.list_widget)

        self.search_edit.textChanged.connect(self._on_text_changed)
        self.search_edit.returnPressed.connect(self._accept_current)
        self.list_widget.itemActivated.connect(
            lambda _: self._accept_current()
        )

    def _search_nodes(self, query: str) -> List[NodeDefinition]:

        if not query:
            result = sorted(self._all_nodes,
                            key=lambda nd: nd.node_label.lower())
            return result[: self._result_limit]

        q = query.lower()

        filtered = [
            nd
            for nd in self._all_nodes
            if q in nd.node_label.lower()
        ]

        filtered.sort(key=lambda nd: nd.node_label.lower())
        return filtered[: self._result_limit]

    def _update_list(self, query: str):
        self.list_widget.clear()
        self._current_results = self._search_nodes(
            query)

        for nd in self._current_results:
            item = QtWidgets.QListWidgetItem(
                nd.node_label, self.list_widget)
            item.setToolTip(f"{nd.node_context} | {nd.node_type}")

        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _on_text_changed(self, text: str):
        self._update_list(text)

    def _accept_current(self):
        if self.list_widget.currentRow() < 0:
            return
        self.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.reject()
            return
        super().keyPressEvent(event)

    def selected_node(self) -> NodeDefinition | None:
        if not hasattr(self, "_current_results"):
            return None
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self._current_results):
            return None
        return self._current_results[row]
