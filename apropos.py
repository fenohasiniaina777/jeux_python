from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import QPropertyAnimation, QRect, Qt
from PyQt6.QtGui import QFontDatabase
import sys

class AproposPage(QLabel):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("À propos")
        self.setGeometry(550, 130, 600, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) #headless
        self.initUI()

        # charger la police
        QFontDatabase.addApplicationFont("./fonts/Digital-7 Mono.ttf")

    def initUI(self):
        # Création d'un label pour le texte "À propos"
        self.label = QLabel("Bienvenue ! \n Piozla est un projet realise avec PyQt6. \n Developpe par le groupe Hertz \n\n\n\n Α hertz@gmail.com", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(50, 60, 530, 200)  # Position initiale hors de la fenêtre
        self.label.setStyleSheet("font-family: 'Digital-7 Mono', 'Courier New', monospace; color: white; font-size: 20px; font-weight: bold; background-color: transparent;")

        # images
        self.image = QLabel(self)
        self.image.setGeometry(0,0,600,600)
        self.image.setStyleSheet("background-image: url(./images/png/tissus/tissu3.webp); background-position: center;")


        self.label.raise_()

        # Animation de descente
        self.animation = QPropertyAnimation(self.label, b"geometry")
        self.animation.setDuration(10000)  # Durée de l'animation en millisecondes
        self.animation.setLoopCount(-1)
        self.animation.setStartValue(QRect(50, 60, 515, 200))  # Position de départ
        self.animation.setEndValue(QRect(50, 440, 515, 200))  # Position finale
        self.animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AproposPage()
    window.show()
    sys.exit(app.exec())