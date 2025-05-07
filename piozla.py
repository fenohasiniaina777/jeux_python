from PyQt6.QtWidgets import QWidget,QFileDialog,QGraphicsDropShadowEffect,QApplication,QMessageBox,QLabel,QPushButton,QFrame,QCheckBox
from PyQt6.QtGui import QPixmap,QIcon,QImage,QFontDatabase
from PyQt6.QtCore import QSize,Qt,QTimer
import sys,os,shutil, random
from apropos import AproposPage
from data import get_joueur


import pygame.mixer

class AnimationButton(QPushButton):
    def __init__(self, text="", parent= None):
        super().__init__(text, parent)
        self.setFixedSize(200,50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("color: white; font-size: 24px; border-radius: 15px;")
        self.offset = 0
        self.timer =QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(100)

    def animate(self):
        self.offset =(self.offset + 5 ) % 200 #loop the offset
        gradient_style = f"""
            QPushButton {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(90,24,154,255),
                    stop:{(self.offset % 200)/200:.2f} rgba(255,255,255,180),
                    stop:{((self.offset+40) % 200)/200:.2f} rgba(90,24,154,255),
                    stop:1 rgba(90,24,154,255)
                );
                color: white;
                font-family: 'Digital-7', 'Courier New', monospace;
                font-size: 15px;
                font-weight: bold;
                border:1px solid rgba(7, 0, 104,0.9);
                border-radius: 15px;
                padding: 10px;
            }}
            QPushButton:hover{{
                font-size: 24px;
                font-weight: bold;
            }}
            
        """
        self.setStyleSheet(gradient_style)

class Piozla(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(450,50,800,800)
        self.setWindowTitle("piozla")

        # charger la police
        QFontDatabase.addApplicationFont("./fonts/Digital-7 Mono.ttf")

        # image de fond
        self.img_fond = QPixmap("./images/png/tissus/taquin6.png")
        label_img_fond = QLabel(self)
        label_img_fond.setFixedSize(800,800)
        label_img_fond.setScaledContents(True)
        taille_img_font = self.img_fond.scaled(800,800,Qt.AspectRatioMode.KeepAspectRatio)
        label_img_fond.setPixmap(taille_img_font)

        self.volume_value = 0.3  # volume par défaut
        


        # son
        pygame.mixer.init()
        pygame.mixer.music.load("./audio/01- Concerto pour une voix.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.volume_value)



        self.label_titre = QLabel("Niveau du jeu", self)
        self.label_titre.setStyleSheet("font-size: 40px;color:white ;font-family: 'Digital-7 Mono', 'Courier New', monospace; font-weight: bold;align-items: center;")
        self.label_titre.setGeometry(230,100,350,80)


        # label coins
        self.frame_coins = QFrame(self)
        self.frame_coins.setGeometry(590,60,150,40)
        self.frame_coins.setStyleSheet("background-color: black; border: none;border-radius: 15px")

            # recuperation donnees joueur 
        player_data = get_joueur()
        argent = player_data[3]

        self.label_coins = QLabel(f"{argent}",self.frame_coins)
        self.label_coins.setGeometry(0,0,150,40)
        self.label_coins.setStyleSheet("color: gold; font-size: 30px;padding-left: 10px; font-family: 'Digital-7 Mono', 'Courier New', monospace;")

        # icon coins
        self.icon_coin = QPushButton(self.frame_coins)
        self.icon_coin.setGeometry(110,5,30,30)
        self.icon_coin.setIcon(QIcon("./images/png/coins/gold33.png"))
        self.icon_coin.setIconSize(QSize(30,30))
        self.icon_coin.setStyleSheet("background-color: transparent; ")
        
       
        


        # bouton acheter pack
        self.btn_magasin = QPushButton("", self)
        self.btn_magasin.setGeometry(660,670,100,100)
        self.btn_magasin.setStyleSheet("background-color: transparent;")
        self.btn_magasin.setIcon(QIcon("./images/png/kit2.png"))
        self.btn_magasin.setIconSize(QSize(100,100))
        self.btn_magasin.setCursor(Qt.CursorShape.PointingHandCursor)

        # connexion bouton magasin
        self.btn_magasin.clicked.connect(self.open_boutic)

        # bouton importer photo
        self.btn_import_img = QPushButton(self)
        self.btn_import_img.setGeometry(100,695,50,50)
        self.btn_import_img.setStyleSheet("background-color: transparent;")
        self.btn_import_img.setIcon(QIcon("./images/png/upload"))
        self.btn_import_img.setIconSize(QSize(50,50))
        self.btn_import_img.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_import_img.setToolTip("Importer votre fichier image ici")
        
        self.btn_import_img.clicked.connect(self.upload_image)


        # btn jouer au hasard
        self.btn_jouer_hasard = QPushButton(self)
        self.btn_jouer_hasard.setGeometry(350,550,100,100)
        self.btn_jouer_hasard.setStyleSheet("background-color: transparent; align-items:center;")
        self.btn_jouer_hasard.setIcon(QIcon("./images/png/btn/random2.png"))
        self.btn_jouer_hasard.setIconSize(QSize(100,100))
        self.btn_jouer_hasard.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_jouer_hasard.setToolTip("Jouer au hasard")

        self.btn_jouer_hasard.clicked.connect(self.jouer_au_hasard)



        # label choisir niveau
        niveaux = ["Débutant", "Intermédiaire", "Avancé", "Expert"]
        for i ,niveau in enumerate(niveaux):
            button = AnimationButton(niveau, self)
            button.move(300,200 + i *90)


            # connexion au niveau
            button.clicked.connect(lambda checked, n = niveau: self.choisir_niveau(n))

            


        # btn_a_propos
        self.btn_a_propos = QPushButton(self)
        self.btn_a_propos.setGeometry(55,695,50,50)
        self.btn_a_propos.setIcon(QIcon("./images/png/question1.png"))
        self.btn_a_propos.setIconSize(QSize(50,50))
        self.btn_a_propos.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_a_propos.setStyleSheet("background-color: transparent; ")

        # afficher le frame page apropos
        self.btn_a_propos.setMouseTracking(True)
        self.btn_a_propos.enterEvent = self.show_a_propos
        self.btn_a_propos.leaveEvent = self.hide_a_propos

    

        # volume du jeu
        self.volume_check = QCheckBox(" Audio",self)
        self.volume_check.setGeometry(150,700,200,60)
        self.volume_check.setStyleSheet("""
             QCheckBox {
                color: white;
                font-size: 25px;
                padding: 10px;
                font-family: 'Digital-7 Mono', 'Courier New', monospace;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
                                        
                    """)
        self.volume_check.setCheckState(Qt.CheckState.Checked)
        # connexion de signal
        self.volume_check.stateChanged.connect(self.play_audio)

        # image casque
        self.headphone= QPushButton(self)
        self.headphone.setGeometry(280,700,50,50)
        self.headphone.setIcon(QIcon("./images/png/headphone3.png"))
        self.headphone.setIconSize(QSize(50,50))
        self.headphone.setStyleSheet("background-color: transparent;")


        self.btn_quitter = QPushButton("",self)
        self.btn_quitter.setGeometry(380,680,40,40)
        self.btn_quitter.setIcon(QIcon("./images/png/btn/quitter.png"))
        self.btn_quitter.setIconSize(QSize(40,40))
        self.btn_quitter.setStyleSheet("background-color: transparent;")
    
        self.btn_quitter.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_quitter.clicked.connect(self.quit)
     # ombre au boutons
        boutons = [self.label_coins, self.btn_quitter, self.label_titre,self.btn_magasin, self.btn_import_img,self.btn_jouer_hasard, self.btn_a_propos,self.headphone]
        
        for bouton in boutons:
            shadow_effect = QGraphicsDropShadowEffect(self)
            shadow_effect.setBlurRadius(20)
            shadow_effect.setOffset(10,10)
            shadow_effect.setColor(Qt.GlobalColor.black)

            bouton.setGraphicsEffect(shadow_effect)


    # afficher a propos
    def show_a_propos(self, event):
        self.page_a_propos  = AproposPage()
        self.page_a_propos.setVisible(True)

    def hide_a_propos(self, event):
        self.page_a_propos.setVisible(False)

   
    # importer une image
    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importer une image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp)"
        )


        if file_path:
            image = QImage(file_path)
            if image.isNull():
                QMessageBox.warning(self,  "Erreur", "Impossible de charger l'image.")
                return

            width = image.width()
            height = image.height()

            if width != height:
                QMessageBox.warning(self, "Image invalide", "L'image doit être carrée (même largeur et hauteur).")
                return
            
            try:
                os.makedirs("images", exist_ok = True)

                filename = os.path.basename(file_path)

                dest_path = os.path.join("images", filename)
                # copier le fichier
                shutil.copy(file_path, dest_path)
                QMessageBox.information(self, "Succès", f"Image {filename} a été importée")

            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'importation : {str(e)}")

    def ajuster_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
        print(f"Volume ajusté à {volume}")
        
    # play audio
    def play_audio(self):
        if self.volume_check.isChecked():
            print("Audio activé")

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)  # relancer la musique en boucle

            pygame.mixer.music.set_volume(self.volume_value)  # bonne échelle (0.0 - 1.0)

        else:
            print("Audio désactivé")
            pygame.mixer.music.set_volume(0.0) # volume à zéro

# Ouvrir la boutique
    def open_boutic(self):
        checkbox_state = self.volume_check.isChecked() #recuperer l'etat de checkbox

        self.close()
        from pack import Pack
        self.win_pack = Pack(checkbox_state, self)
        self.win_pack.show()

# ouvrir niveau 
    def choisir_niveau(self, niveau):
        checkbox_state = self.volume_check.isChecked() #recuperer l'etat de checkbox

        print(f"{niveau}")
        if niveau == "Débutant":
            self.close()
            from level1 import Piozla_level1
            self.win_level1 = Piozla_level1(checkbox_state, self)
            self.win_level1.show()

        elif niveau == "Intermédiaire":
            self.close() 
            from level2 import Piozla_level2
            self.win_level2 = Piozla_level2(checkbox_state, self)
            self.win_level2.show()
            

        elif niveau == "Avancé":
            self.close()
            from level3 import Piozla_level3
            self.win_level3 = Piozla_level3(checkbox_state, self)
            self.win_level3.show()
            
        
        elif niveau == "Expert":
            print("attend")
            self.close()
            from level4 import Piozla_level4
            self.win_level4 = Piozla_level4(checkbox_state, self)
            self.win_level4.show()

    # appeler le niveau suivant
    def aller_niveau_suivant(self, niveau_suivant):
        print(niveau_suivant)
        self.choisir_niveau(niveau_suivant)


    def jouer_au_hasard(self):
        niveaux= ["Débutant", "Intermédiaire", "Avancé", "Expert"]
        self.tirage_index = 0

        self.tirage_timer = QTimer(self)
        self.tirage_timer.setInterval(300)
        
        def tirage_step():
            niveau_temps = random.choice(niveaux)
            if self.tirage_index < 2 :
                self.tirage_index += 1

            else:
                self.tirage_timer.stop()
                niveau_final = niveau_temps
                self.choisir_niveau(niveau_final)
        self.tirage_timer.timeout.connect(tirage_step)
        self.tirage_timer.start()

    def quit(self):
        from messages import quitter
        if quitter(parent=self):
            self.close()
        else:
            return


       
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win  = Piozla()
    win.show()
    sys.exit(app.exec())