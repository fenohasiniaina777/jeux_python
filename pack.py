import os
from PyQt6.QtWidgets import QApplication,QLabel,QPushButton,QFrame,QMessageBox
from PyQt6.QtGui import QPixmap,QPainter,QPainterPath,QIcon,QFontDatabase
from PyQt6.QtCore import Qt,QRectF,QSize,QUrl
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer

from data import get_joueur, update_boite, update_joueur
import sys

def pixmap_rounded(pixmap, radius):
    size = pixmap.size()
    rounded = QPixmap(size)
    rounded.fill(Qt.GlobalColor.transparent)

    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    path = QPainterPath()
    path.addRoundedRect(QRectF(0, 0, size.width(), size.height()), radius, radius)

    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    return rounded
class Pack(QFrame):
    def __init__(self, checkbox_state, parent):
        super().__init__()
        self.setWindowTitle("Boutique de Packs")
        self.setFixedSize(700,300)
        self.setStyleSheet("background-color: rgb(45, 77, 142)")

        self.parent = parent

        # son
        self.son_ok = QAudioOutput()
        self.son_error =QAudioOutput()
        

        # etat volume
        self.volume_state = checkbox_state

        if self.volume_state:
            self.parent.ajuster_volume(0.0)
            self.son_ok.setVolume(1)
            self.son_error.setVolume(1)
            
            print("son active")
        else:
            self.son_ok.setVolume(0.0)
            self.son_error.setVolume(0.0)
            
            print("son desactive")
        
        # init son
        self.audio_ok= QMediaPlayer()
        self.audio_ok.setAudioOutput(self.son_ok)
        self.audio_ok.setSource(QUrl.fromLocalFile("./audio/magic-strike-5856.mp3"))

        self.audio_error = QMediaPlayer()
        self.audio_error.setAudioOutput(self.son_error)
        self.audio_error.setSource(QUrl.fromLocalFile("./audio/error_sound-221445.mp3"))



        # charger la police
        QFontDatabase.addApplicationFont("./fonts/Digital-7 Mono.ttf")

        self.boites = []
        self.creer_boite()

        # bouton retour au menu
        self.btn_retour  = QPushButton("", self)
        self.btn_retour.setGeometry(10,5,50,50)
        self.btn_retour.setIcon(QIcon("./images/png/return.webp"))
        self.btn_retour.setIconSize(QSize(50,50))
        self.btn_retour.setStyleSheet("background-color: transparent;")

        # connexion btn retour
        self.btn_retour.clicked.connect(self.aller_menu)

    # MESSAGEBOX
    def achat_reussi(self, prix):
        self.audio_ok.play()
        msg = QMessageBox()
        msg.setWindowTitle("Achat réussi")
        msg.setText(f"Vous avez acheté un pack de <b>{prix}</b>!")
        msg.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        msg.setStyleSheet("""
            QMessageBox {
                font-family: 'Digital-7 Mono', 'Courier New', monospace;
                font-size: 20px;
                background-color: white;
                color: white;
                border: 2px solid green;
            }
            QPushbutton{
                background-color: white;
                color: black;
                border: 1px solid gray;
                padding: 5px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                color: black;
            }
                          """)
        msg.exec()

        
    def achat_annule(self, prix):
        self.audio_error.play()
        msg = QMessageBox()
        msg.setWindowTitle("Achat annulé")
        msg.setText(f"Achat échoué : Solde insuffisant pour acheter la boîte à {prix}.")
        msg.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        msg.setStyleSheet("""
            QMessageBox {
                font-family: 'Digital-7 Mono', 'Courier New', monospace;
                font-size: 20px;
                background-color: white;
                color: white;
                border: 2px solid green;
            }
            QPushbutton{
                background-color: white;
                color: black;
                border: 1px solid gray;
                padding: 5px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                color: black;
            }
                          """)
        msg.exec()
    
    def reopen_page(self):
        self.creer_boite()
        self.show()

    def aller_menu(self):
        self.close()
        from piozla import Piozla
        self.win_menu = Piozla()
        self.win_menu.show()

    def get_img_path(self,index):
        extensions = ['.png', '.jpg', '.jpeg','.webp']
        for ext in extensions:
            path = f"./images/png/pack/{index}{ext}"
            if os.path.exists(path):
                return path
        return None

   

    def creer_boite(self):
        couleurs= ["#FF4C4C", "#4C9AFF","#4CAF50","#FF9800"]
        couleurs_nbr= ["#4CAF50","#FF9800","#FF4C4C", "#4C9AFF"]
        prix_boite = ["10$", "5$", "2$","100$"]
        for i in range(4):
            boite = QLabel(self)
            boite.setGeometry(50 + i * 150, 80, 100,150)
            boite.setStyleSheet(f"background-color:{couleurs[i]}; border-radius: 10px;")

            img = QLabel(boite)
            img.setGeometry(5,5,90,90)
            img.setStyleSheet("background-color: transparent;")

            img_path = self.get_img_path(i)

            if img_path:

                try:
                    pixmap = QPixmap(img_path).scaled(
                        90,90, 
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    rounded_pixmap = pixmap_rounded(pixmap, 15)
                    img.setPixmap(rounded_pixmap)

                except Exception as e:
                    img.setText("Image\nintrouvable")
                    img.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                img.setAlignment(Qt.AlignmentFlag.AlignCenter)
                # img.setText(f"img {i+1}")

            # span couleur
            compteur = QLabel(boite)
            compteur.setGeometry(60,10,30,30)
            compteur.setStyleSheet(
            f"background-color: {couleurs_nbr[i]}; color: white; border-radius: 15px; font-size: 15px; text-align: center;font-weight: bold;"
            )
            compteur.setAlignment(Qt.AlignmentFlag.AlignCenter)
            

                # recuperation des donnees
            joueur = get_joueur()
            if joueur:
                _, _, _, _, add_temps_count, dim_nbr_pas_count, shuffle_count, special_count = joueur
                valeurs = [add_temps_count,dim_nbr_pas_count,shuffle_count,special_count]
                print(valeurs[1]+1,valeurs[2])
                compteur.setText(str(valeurs[i]))

            bouton = QPushButton(prix_boite[i], boite)
            bouton.setGeometry(5, 100, 90, 40)
            bouton.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: black;
                    border: 1px solid gray;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 15px;
                    font-family: 'Digital-7 Mono', 'Courier New', monospace;
                }

                QPushButton:hover {
                    background-color: #e0e0e0;
                }

            """)
            bouton.setToolTip("Acheter ce bonus")

            # connexion bouton
            bouton.clicked.connect(lambda _, index=i, prix= prix_boite[i]:self.gerer_achat(index, prix))

            self.boites.append((boite, img, bouton))

    def gerer_achat(self, index, prix):
        # recup les donnees du joueur
        joueur = get_joueur()
        if joueur is None:
            QMessageBox.warning(self, "Erreur", "Aucun joueur trouvé dans la base de données.")
            return
        
        joueur_id, temps, nb_pas, argent, boite1, boite2, boite3, boite4 = joueur
        prix_int = int(prix.replace("$", "")) #convertir le prix en int

        # verifier si le joueur a assez d'argent
        if argent >= prix_int:
            nouvel_argent = argent - prix_int
            temps = temps
            nb_pas = nb_pas
            update_joueur(temps, nb_pas, nouvel_argent, boite1, boite2, boite3, boite4)


            update_boite(joueur_id, index)


            
            print(f"Boite {index} achetee pour {prix}")
            self.achat_reussi(prix)      
            self.close()
            self.reopen_page()
        else:
             # Afficher un message d'erreur si le joueur n'a pas assez d'argent
            self.achat_annule(prix)
            print(f"Achat échoué : Solde insuffisant ({argent}€) pour acheter la boîte {index} à {prix}.")
    
        # # boutiques
        # # BOITE 1
        # self.boite1 = QLabel(self)
        # self.boite1.setGeometry(50,50,100,150)
        # self.boite1.setStyleSheet("background-color: red")

        # self.img1 = QLabel(self.boite1)
        # self.img1.setGeometry(5,5,90,90)
        # self.img1.setStyleSheet("background-color: green")

        # self.btn_1 = QPushButton("Acheter", self.boite1)
        # self.btn_1.setGeometry(5,100,90,50)
        # self.btn_1.setStyleSheet("background-color: white; color:black")

        #  # BOITE 2
        # self.boite2 = QLabel(self)
        # self.boite2.setGeometry(200,50,100,150)
        # self.boite2.setStyleSheet("background-color: red")

        # self.img2 = QLabel(self.boite2)
        # self.img2.setGeometry(5,5,90,90)
        # self.img2.setStyleSheet("background-color: green")

        # self.btn_2 = QPushButton("Acheter", self.boite2)
        # self.btn_2.setGeometry(5,100,90,50)
        # # self.btn_2.setStyleSheet("background-color: white; color:black")

        #  # BOITE 3
        # self.boite3 = QLabel(self)
        # self.boite3.setGeometry(350,50,100,150)
        # self.boite3.setStyleSheet("background-color: red")

        # self.img3 = QLabel(self.boite3)
        # self.img3.setGeometry(5,5,90,90)
        # self.img3.setStyleSheet("background-color: green")

        # self.btn_3 = QPushButton("Acheter", self.boite3)
        # self.btn_3.setGeometry(5,100,90,50)
        # self.btn_3.setStyleSheet("background-color: white; color:black")

        #  # BOITE 4
        # self.boite4 = QLabel(self)
        # self.boite4.setGeometry(500,50,100,150)
        # self.boite4.setStyleSheet("background-color: red")

        # self.img4 = QLabel(self.boite4)
        # self.img4.setGeometry(5,5,90,90)
        # self.img4.setStyleSheet("background-color: green")

        # self.btn_4 = QPushButton("Acheter", self.boite4)
        # self.btn_4.setGeometry(5,100,90,50)
        # self.btn_4.setStyleSheet("background-color: white; color:black")

           






if __name__ == '__main__':
    app = QApplication(sys.argv)
    win  = Pack()
    win.show()
    sys.exit(app.exec())