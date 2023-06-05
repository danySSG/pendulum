from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QSlider,
    QLabel,
    QMenuBar,
    QStatusBar,
    QApplication,
    QMainWindow,
)
from PyQt5.QtCore import QThread, QRect, Qt, QMetaObject, QCoreApplication
from PyQt5.QtGui import QIcon

from manim.utils.file_ops import open_file as open_media_file
from styles import general_style, anime_button, pdf_button
from animation import Phase_Space
from os import startfile, path
from shutil import rmtree


class AnimationThread(QThread):
    def __init__(self, scene):
        QThread.__init__(self)
        self.scene = scene

    def run(self):
        self.scene.render()
        open_media_file(self.scene.renderer.file_writer.movie_file_path)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Проверить, существует ли директория
        if path.exists("media/videos"):
            # Если существует, то удалить
            rmtree("media/videos")

        MainWindow.setStyleSheet(general_style)
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(580, 310)  # Запрет изменения размера окна
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_button = QPushButton(self.centralwidget)
        self.main_button.setStyleSheet(anime_button)
        self.main_button.setGeometry(QRect(15, 220, 210, 60))
        self.main_button.setObjectName("main_button")

        self.pdf_button = QPushButton(self.centralwidget)
        self.pdf_button.setStyleSheet(pdf_button)
        self.pdf_button.setGeometry(QRect(235, 220, 340, 60))
        self.pdf_button.setObjectName("pdf_button")

        self.angle_slider = QSlider(self.centralwidget)
        self.angle_slider.setGeometry(QRect(20, 20, 200, 20))
        self.angle_slider.setMinimum(-314)
        self.angle_slider.setMaximum(314)
        self.angle_slider.setProperty("value", 271)
        self.angle_slider.setOrientation(Qt.Horizontal)
        self.angle_slider.setObjectName("angle_slider")

        self.friction_slider = QSlider(self.centralwidget)
        self.friction_slider.setGeometry(QRect(20, 60, 200, 20))
        self.friction_slider.setMaximum(100)
        self.friction_slider.setProperty("value", 35)
        self.friction_slider.setOrientation(Qt.Horizontal)
        self.friction_slider.setObjectName("friction_slider")

        self.mass_slider = QSlider(self.centralwidget)
        self.mass_slider.setGeometry(QRect(20, 100, 200, 20))
        self.mass_slider.setMaximum(100)
        self.mass_slider.setSingleStep(1)
        self.mass_slider.setProperty("value", 50)
        self.mass_slider.setOrientation(Qt.Horizontal)
        self.mass_slider.setObjectName("mass_slider")

        self.gravity_slider = QSlider(self.centralwidget)
        self.gravity_slider.setGeometry(QRect(20, 140, 200, 20))
        self.gravity_slider.setMaximum(100)
        self.gravity_slider.setProperty("value", 10)
        self.gravity_slider.setOrientation(Qt.Horizontal)
        self.gravity_slider.setObjectName("gravity_slider")

        self.time_slider = QSlider(self.centralwidget)
        self.time_slider.setGeometry(QRect(20, 180, 200, 20))
        self.time_slider.setMaximum(100)
        self.time_slider.setProperty("value", 30)
        self.time_slider.setOrientation(Qt.Horizontal)
        self.time_slider.setObjectName("time_slider")

        self.label_1 = QLabel(self.centralwidget)
        self.label_1.setGeometry(QRect(240, 20, 330, 20))
        self.label_1.setObjectName("label_1")

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QRect(240, 60, 330, 20))
        self.label_2.setObjectName("label_2")

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setGeometry(QRect(240, 100, 330, 20))
        self.label_3.setObjectName("label_3")

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setGeometry(QRect(240, 140, 330, 20))
        self.label_4.setObjectName("label_4")

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setGeometry(QRect(240, 180, 330, 20))
        self.label_5.setObjectName("label_5")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 380, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        self.add_functions()

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Маятник"))
        MainWindow.setWindowIcon(QIcon("icon.ico"))
        self.main_button.setText(_translate("MainWindow", "Анимировать"))
        self.pdf_button.setText(_translate("MainWindow", "Читать теорию"))
        self.label_1.setText(
            _translate(
                "MainWindow", f"Начальный угол: {self.angle_slider.value()/100} rad"
            )
        )
        self.label_2.setText(
            _translate("MainWindow", f"Трение: {self.friction_slider.value()/100}")
        )
        self.label_3.setText(
            _translate("MainWindow", f"Масса: {self.mass_slider.value()/10} кг")
        )
        self.label_4.setText(
            _translate(
                "MainWindow",
                f"Ускорение свободного падения: {self.gravity_slider.value()/10} м/с^2",
            )
        )
        self.label_5.setText(
            _translate(
                "MainWindow", f"Время симуляции: {self.time_slider.value()} секунд"
            )
        )

    def add_functions(self):
        self.main_button.clicked.connect(self.make_animation)

        self.pdf_button.clicked.connect(self.open_pdf)

        self.angle_slider.valueChanged.connect(self.change_label_1)
        self.friction_slider.valueChanged.connect(self.change_label_2)
        self.mass_slider.valueChanged.connect(self.change_label_3)
        self.gravity_slider.valueChanged.connect(self.change_label_4)
        self.time_slider.valueChanged.connect(self.change_label_5)

    def open_pdf(self):
        startfile("theory.pdf")

    def make_animation(self):
        self.main_button.setEnabled(False)
        self.main_button.setText("Анимация готовится...")
        self.main_button.setStyleSheet("background-color: grey;")
        scene = Phase_Space(
            self.angle_slider.value() / 100,
            self.mass_slider.value() / 10,
            self.gravity_slider.value() / 10,
            self.friction_slider.value() / 100,
            self.time_slider.value(),
        )
        self.thread = AnimationThread(scene)
        self.thread.finished.connect(self.on_animation_finished)
        self.thread.start()

    def on_animation_finished(self):
        self.main_button.setEnabled(True)
        self.main_button.setText("Анимировать")
        self.main_button.setStyleSheet("background-color: #ff5a1f;")

    def change_label_1(self):
        self.label_1.setText(f"Начальный угол: {self.angle_slider.value()/100} rad")

    def change_label_2(self):
        self.label_2.setText(f"Трение: {self.friction_slider.value()/100}")

    def change_label_3(self):
        self.label_3.setText(f"Масса: {self.mass_slider.value()/10} кг")

    def change_label_4(self):
        self.label_4.setText(
            f"Ускорение свободного падения: {self.gravity_slider.value()/10} м/с^2"
        )

    def change_label_5(self):
        self.label_5.setText(f"Время симуляции: {self.time_slider.value()} секунд")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
