"""
PyCalc is a simple calculator GUI built using PyQt6 and
https://realpython.com/python-pyqt-gui-calculator/ tutorial
"""
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QGridLayout, QLineEdit, QPushButton,
                             QVBoxLayout)
from functools import partial

WINDOW_SIZE= 235
DISPLAY_HEIGHT= 35
BUTTON_SIZE= 40
ERROR_MSG= "ERROR"

"""         PyCalc uses MODEL-VIEW-CONTROLLER framework      """


class PyCalcWindow(QMainWindow):
    """         This is PyCalc's VIEW class         """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout= QVBoxLayout()
        centralWidget=QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display= QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap={}
        buttonsLayout= QGridLayout()
        keyBoard= [
            ["7","8","9","/","C"],
            ["4","5","6","*","("],
            ["1","2","3","-",")"],
            ["0","00",".","+","="],
        ]

#       row=item index, keys= actual item,  keyBoard=iterable list/set/etc.
        for row, keys in enumerate(keyBoard):
            #  col=item index, key= actual item,  keys=iterable list/set/etc.
            for col, key in enumerate(keys):
                self.buttonMap[key]= QPushButton('name' +key)  # I think that THIS is the line that links the button label to the button value.
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)

        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        """         Set the display's text.         """
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """         Get the display's text.         """
        return self.display.text()

    def clearDisplay(self):
        """         Clear the display.      """
        self.setDisplayText("")


def evalExpression(expression):
    """         This is PyCalc's MODEL class.       """

    try:
        result= str(eval(expression,{}, {}))
    except Exception:
        result= ERROR_MSG
    return result


class PyCalc:
    """
    This is PyCalc's CONTROLLER class. It will:
    1. Access the GUI's public interface.
    2. Handle the creation of math expressions.
    3. Connect the buttons' .clicked signals to appropriate slots
    """

    def __init__(self, model, view):
        """Make instance attributes of evalExpression method (MODEL) & PyCalcWindow Class (VIEW), then wire everything up."""
        self._evaluate= model
        self._view= view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        """Evaluate the expression that user just typed in Update display text w/computation result"""
        result= self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        """Builds the math expression in STRING form by concatenating initial
           display value with the user's input, one button click at a time,
           and then updates the display with each new input."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression= self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        """Connects the all of the buttons' .clicked signals w/ the appropriate slots methods in Controller Class"""
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=","C"}:
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)


def main():
    """PyCalc's Main function."""
    pycalcApp = QApplication([])
    pycalcWindow= PyCalcWindow()
    pycalcWindow.show()
    PyCalc(model=evalExpression, view=pycalcWindow)
    sys.exit(pycalcApp.exec())


if __name__ == "__main__":
    """PyCalc's Main function."""
    print('\nRunning PyCalc app now!\n')
    main()
