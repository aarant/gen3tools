""" TableWidget with data exportable to Excel/spreadsheet programs

Based on https://stackoverflow.com/a/60716389
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class CopyableTableWidget(QTableWidget):
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            grid = {}
            for index in self.selectedIndexes():
                grid.setdefault(index.row(), set()).add(index.column())
            rows = []
            for r, cols in sorted(grid.items()):
                rows.append('\t'.join(self.item(r, c).text() for c in cols))
            text = '\n'.join(rows)
            self.clipboard.setText(text)
