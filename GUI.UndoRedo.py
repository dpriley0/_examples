import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QUndoStack, QUndoCommand

class MyUndoCommand(QUndoCommand):
    def __init__(self, text, undo_function, redo_function):
        super().__init__(text)
        self._undo_function = undo_function
        self._redo_function = redo_function

    def undo(self):
        self._undo_function()

    def redo(self):
        self._redo_function()

class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.undo_stack = QUndoStack()

        self.initUI()

    def initUI(self):
        undo_action = QAction('Undo', self)
        undo_action.triggered.connect(self.undo_stack.undo)
        redo_action = QAction('Redo', self)
        redo_action.triggered.connect(self.undo_stack.redo)

        self.menu = self.menuBar()
        self.edit_menu = self.menu.addMenu('Edit')
        self.edit_menu.addAction(undo_action)
        self.edit_menu.addAction(redo_action)

        self.setWindowTitle('Undo/Redo Example')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApplication()
    sys.exit(app.exec_())