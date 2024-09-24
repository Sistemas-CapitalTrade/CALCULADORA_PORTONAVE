import sys
import math
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QGridLayout
from PySide6.QtCore import Qt, Slot

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora - Capital Trade")
        self.setWindowIcon(QIcon('ícone2.ico'))  # Define o ícone da janela principal

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color: black;")

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.text_display = QLineEdit()
        self.text_display.setStyleSheet("background-color: black; color: #ffffff; border: none; font-size: 24px;")
        self.text_display.setAlignment(Qt.AlignRight)
        self.text_display.setMinimumHeight(80)
        self.layout.addWidget(self.text_display)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)  # Adiciona espaçamento entre os botões

        buttons = [
            ("7", self.number_clicked),
            ("8", self.number_clicked),
            ("9", self.number_clicked),
            ("/", self.operator_clicked),
            ("4", self.number_clicked),
            ("5", self.number_clicked),
            ("6", self.number_clicked),
            ("*", self.operator_clicked),
            ("1", self.number_clicked),
            ("2", self.number_clicked),
            ("3", self.number_clicked),
            ("-", self.operator_clicked),
            ("0", self.number_clicked),
            (".", self.number_clicked),
            ("=", self.calculate_result),
            ("+", self.operator_clicked),
            ("(", self.number_clicked),
            (")", self.number_clicked),
            ("sin", self.trigonometric_function_clicked),
            ("cos", self.trigonometric_function_clicked),
            ("tan", self.trigonometric_function_clicked),
            ("log", self.logarithmic_function_clicked),
            ("sqrt", self.sqrt_function_clicked),
            ("^", self.power_function_clicked)
        ]

        for position, (label, function) in enumerate(buttons):
            button = RoundButton(label)
            if label.isdigit() or label in [".", "="]:  # Altera a cor dos botões numéricos, ".", e "="
                button.setStyleSheet("font-size: 18px; background-color: #d63600; color: #ffffff;")
            else:
                button.setStyleSheet("font-size: 18px; background-color: #002060; color: #ffffff;")
            button.clicked.connect(function)
            row = position // 4
            column = position % 4
            grid_layout.addWidget(button, row, column)

        self.layout.addLayout(grid_layout)

        self.clear_display()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:  # Verifica se a tecla pressionada é Enter
            self.calculate_result()
        elif event.key() == Qt.Key_Escape:
            self.clear_display()

    @Slot()
    def number_clicked(self):
        clicked_button = self.sender()
        self.text_display.setText(self.text_display.text() + clicked_button.text())

    @Slot()
    def operator_clicked(self):
        clicked_button = self.sender()
        self.text_display.setText(self.text_display.text() + " " + clicked_button.text() + " ")

    @Slot()
    def calculate_result(self):
        expression = self.text_display.text()
        try:
            # Correção para avaliar corretamente as funções trigonométricas e a raiz quadrada
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("log", "math.log")  # Correção para a função log()
            expression = expression.replace("sqrt", "math.sqrt")
            expression = expression.replace("^", "**")
            # Avalia a expressão usando o eval(), mas substitui os nomes das funções pelas da biblioteca math
            result = eval(expression)
            self.text_display.setText(str(result))
        except Exception as e:
            self.text_display.setText("Erro")

    @Slot()
    def clear_display(self):
        self.text_display.clear()

    @Slot()
    def trigonometric_function_clicked(self):
        clicked_button = self.sender()
        function = clicked_button.text()
        expression = self.text_display.text() + function + "("
        self.text_display.setText(expression)

    @Slot()
    def logarithmic_function_clicked(self):
        clicked_button = self.sender()
        function = clicked_button.text()
        expression = self.text_display.text() + function + "("
        self.text_display.setText(expression)

    @Slot()
    def sqrt_function_clicked(self):
        clicked_button = self.sender()
        function = clicked_button.text()
        expression = self.text_display.text() + function + "("
        self.text_display.setText(expression)

    @Slot()
    def power_function_clicked(self):
        clicked_button = self.sender()
        function = clicked_button.text()
        expression = self.text_display.text() + "**"
        self.text_display.setText(expression)


class RoundButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet(
            "QPushButton {"
            "border-radius: 20px;"
            "}"
            "QPushButton:hover {"
            "background-color: #d35400;"
            "}"
        )
        self.setMinimumSize(50, 50)
        self.setMaximumSize(100, 100)
        self.setFocusPolicy(Qt.NoFocus)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())