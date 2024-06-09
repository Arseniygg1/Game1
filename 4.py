import sys
import random
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QLabel,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFrame,
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon, QPixmap, QFont


class RussianRouletteMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Русская рулетка')
        self.setWindowIcon(QIcon('path/to/your/icon.ico'))  # Замените "path/to/your/icon.ico" на путь к иконке
        self.setGeometry(300, 200, 400, 200)
        self.setStyleSheet("background-color: #222;")  # Задний фон игры

        layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel("Русская рулетка")
        title_label.setFont(QFont('Arial', 24))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #fff;")
        layout.addWidget(title_label)

        # Кнопки
        buttons_layout = QVBoxLayout()
        buttons_layout.addSpacing(20)

        start_button = QPushButton('Начать игру')
        start_button.setFont(QFont('Arial', 14))
        start_button.setStyleSheet("background-color: #4CAF50; color: #fff; padding: 10px 20px; border: none;")
        start_button.clicked.connect(self.start_game)
        buttons_layout.addWidget(start_button)

        rules_button = QPushButton('Правила игры')
        rules_button.setFont(QFont('Arial', 14))
        rules_button.setStyleSheet("background-color: #008CBA; color: #fff; padding: 10px 20px; border: none;")
        rules_button.clicked.connect(self.show_rules)
        buttons_layout.addWidget(rules_button)

        exit_button = QPushButton('Выход')
        exit_button.setFont(QFont('Arial', 14))
        exit_button.setStyleSheet("background-color: #f44336; color: #fff; padding: 10px 20px; border: none;")
        exit_button.clicked.connect(self.close)
        buttons_layout.addWidget(exit_button)

        layout.addLayout(buttons_layout)
        layout.addStretch(1)

        self.setLayout(layout)

    def start_game(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.close()  # Закрыть меню

    def show_rules(self):
        rules = 'Правила игры:\n\n'
        rules += '1. Игроки сидят вокруг стола и по очереди прокручивают барабан револьвера.\n'
        rules += '2. До тех пор, пока не выстрелит.\n'
        rules += '3. Если револьвер не выстрелил, то игрок выживает, и револьвер передается следующему человеку.\n'
        rules += '4. Если револьвер выстрелил, игрок проигрывает.\n'

        QMessageBox.information(self, 'Правила игры', rules)


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Русская рулетка')
        self.setGeometry(100, 100, 600, 400)  # Увеличили размер окна
        self.setStyleSheet("background-color: #222;")  # Задний фон игры

        layout = QVBoxLayout()

        # Верхний горизонтальный layout для таймера, счетчика и количества игроков
        top_layout = QHBoxLayout()
        top_layout.addStretch(1)  # Расширяем пространство слева

        # 1 - Таймер
        self.timer_label = QLabel('0')
        self.timer_label.setFont(QFont('Arial', 14))
        self.timer_label.setStyleSheet("color: #fff;")
        top_layout.addWidget(self.timer_label)

        top_layout.addStretch(1)  # Расширяем пространство справа

        layout.addLayout(top_layout)

        # 2 - Название игры
        title_label = QLabel("Русская рулетка")
        title_label.setFont(QFont('Arial', 24))
        title_label.setStyleSheet("color: #fff;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # 3 - Счетчик ходов, 4 - Таймер, 5 - Количество игроков
        info_layout = QHBoxLayout()  # Горизонтальный layout для счетчика и таймера
        info_layout.addSpacing(10)

        # 3 - Счетчик ходов
        self.turn_label = QLabel(f"Ход: 0")
        self.turn_label.setFont(QFont('Arial', 14))
        self.turn_label.setStyleSheet("color: #fff;")
        info_layout.addWidget(self.turn_label)

        # 5 - Количество игроков
        self.player_label = QLabel(f"Игроков: 1")
        self.player_label.setFont(QFont('Arial', 14))
        self.player_label.setStyleSheet("color: #fff;")
        info_layout.addWidget(self.player_label)

        info_layout.addSpacing(10)
        layout.addLayout(info_layout)

        # 6 - Игровое поле
        self.game_field = QFrame(self)
        self.game_field.setStyleSheet("background-color: #444; border: 1px solid #fff;")  # Темно-серый фон
        self.game_field_layout = QVBoxLayout()  # Добавляем layout в игровое поле
        self.game_field.setLayout(self.game_field_layout)  # Установка layout'а
        layout.addWidget(self.game_field)

        # 7 - Кнопка выстрела
        self.shoot_button = QPushButton('Выстрелить')
        self.shoot_button.setFont(QFont('Arial', 14))
        self.shoot_button.setStyleSheet("background-color: #f44336; color: #fff; padding: 10px 20px; border: none;")
        self.shoot_button.clicked.connect(self.shoot)
        layout.addWidget(self.shoot_button)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_count = 0
        self.player_count = 1
        self.turn_number = 1

        # Игровое поле
        self.barrel_spin_button = QPushButton('Прокрутить барабан', self)
        self.barrel_spin_button.clicked.connect(self.spin_barrel)
        self.game_field_layout.addWidget(self.barrel_spin_button)

        self.result_label = QLabel('', self)
        self.game_field_layout.addWidget(self.result_label)

        self.bullet_position = random.randint(1, 6)
        self.current_position = 1

    def start_game(self):
        self.timer.start(1000)
        self.timer_count = 0

    def spin_barrel(self):
        self.bullet_position = random.randint(1, 6)
        print(f"Позиция пули в барабане: {self.bullet_position}")

    def shoot(self):
        self.turn_number += 1  # Увеличиваем счетчик ходов после выстрела
        self.turn_label.setText(f"Ход: {self.turn_number}")  # Обновляем текст только один раз

        if self.current_position == self.bullet_position:
            self.result_label.setText('Пуля в барабане! Game over!')
        else:
            self.result_label.setText('Пустой барабан. Ничего не произошло.')

        self.current_position += 1
        if self.current_position > 6:
            self.current_position = 1

    def update_timer(self):
        # self.timer_count += 1
        # self.turn_label.setText(f"Ход: {self.timer_count}")  # Обновляем счетчик ходов
        self.timer_label.setText(str(self.timer_count))  # Обновляем таймер

    def update_timer_label(self, time):
        self.timer_label.setText(str(time))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = RussianRouletteMenu()
    menu.show()
    sys.exit(app.exec())