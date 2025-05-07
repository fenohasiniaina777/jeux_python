from PyQt6.QtWidgets import QLabel, QDialog,QMessageBox
from PyQt6.QtCore import Qt,QTimer,QParallelAnimationGroup,QPropertyAnimation,QRect
from PyQt6.QtGui import QFontDatabase

     # charger la police
QFontDatabase.addApplicationFont("./fonts/Digital-7 Mono.ttf")
# animation pop up 





def message_time_out(parent=None):
    dialog = QDialog(parent)
    dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


    label = QLabel("PERDU!", dialog)
    label.setStyleSheet("font-family: 'Digital-7 Mono', 'Courier New', monospace; color: gold; font-size: 100px; font-weight: bold; background-color: transparent; ")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    anim_pos = QPropertyAnimation(label, b"geometry")
    anim_pos.setDuration(250)
    anim_pos.setStartValue(QRect(550,300,500,500))
    anim_pos.setEndValue(QRect(550,100,500,500))

    anim_pos_ = QPropertyAnimation(label, b"geometry")
    anim_pos_.setDuration(250)
    anim_pos_.setStartValue(QRect(550,100,500,500))
    anim_pos_.setEndValue(QRect(550,100,500,500))

    anim_opac = QPropertyAnimation(label, b"windowOpacity")
    anim_opac.setDuration(5000)
    anim_opac.setStartValue(1)
    anim_opac.setEndValue(0)

    anim_group= QParallelAnimationGroup()
    anim_group.addAnimation(anim_pos)
    anim_group.addAnimation(anim_opac)

    anim_group.finished.connect(dialog.close)
    anim_group.start()

    

    dialog.exec()



def message_win(parent=None):
    dialog = QDialog(parent)
    dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


    label = QLabel("WINNER!", dialog)
    label.setStyleSheet("font-family: 'Digital-7 Mono', 'Courier New', monospace; color: gold; font-size: 100px; font-weight: bold; background-color: transparent; ")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    anim_pos = QPropertyAnimation(label, b"geometry")
    anim_pos.setDuration(250)
    anim_pos.setStartValue(QRect(550,300,500,500))
    anim_pos.setEndValue(QRect(550,100,500,500))

    anim_pos_ = QPropertyAnimation(label, b"geometry")
    anim_pos_.setDuration(250)
    anim_pos_.setStartValue(QRect(550,100,500,500))
    anim_pos_.setEndValue(QRect(550,100,500,500))

    anim_opac = QPropertyAnimation(label, b"windowOpacity")
    anim_opac.setDuration(5000)
    anim_opac.setStartValue(1)
    anim_opac.setEndValue(0)

    anim_group= QParallelAnimationGroup()
    anim_group.addAnimation(anim_pos)
    anim_group.addAnimation(anim_opac)

    anim_group.finished.connect(dialog.close)
    anim_group.start()

    

    dialog.exec()


def retourner_au_menu(parent =None):
    msg = QMessageBox(parent)
    msg.setWindowTitle("Retourner au menu")
    msg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    msg.setGeometry(550,100,500,500)
   
    msg.setText("""
                <span style="color:white;">
                Voulez-vous retourner au menu ?
                </span>
                """)
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg.setDefaultButton(QMessageBox.StandardButton.No)

    msg.setStyleSheet("""
        QMessageBox {
            background-color: #2c3e50;
            color: rgba(90,24,154,255);
            font-family: 'Digital-7 Mono', 'Courier New', monospace;
            font-size: 20px;
            font_weight: bold;
                      
        }
        QMessageBox QPushButton {
            background-color: #2980b9;
            color: white;
            font-family: 'Digital-7 Mono', 'Courier New', monospace;
            font-size: 20px;
        }
        QMessageBox QPushButton:hover {
            background-color: #3498db;
        }
    """)

    repons_user = msg.exec()
    return repons_user ==QMessageBox.StandardButton.Yes




def quitter(parent=None):
    msg = QMessageBox(parent)
    msg.setWindowTitle("Quitter")
    msg.setGeometry(200,300,500,500)
    msg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    msg.setText("""
                <span style="color:white;">
                Voulez-vous quitter ce jeu?
                </span>
                """)
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg.setDefaultButton(QMessageBox.StandardButton.No)

    msg.setStyleSheet("""
        QMessageBox {
            background-color: #2c3e50;
            color: rgba(90,24,154,255);
            font-family: 'Digital-7 Mono', 'Courier New', monospace;
            font-size: 20px;
            font_weight: bold;
                      
        }
        QMessageBox QPushButton {
            background-color: #2980b9;
            color: white;
            font-family: 'Digital-7 Mono', 'Courier New', monospace;
            font-size: 20px;
        }
        QMessageBox QPushButton:hover {
            background-color: #3498db;
        }
    """)

    repons_user = msg.exec()
    return repons_user ==QMessageBox.StandardButton.Yes


