from PyQt6.QtWidgets import QWidget,QApplication,QLabel,QGridLayout,QFrame,QMessageBox,QPushButton
from PyQt6.QtGui import QPixmap,QIcon,QFontDatabase
from PyQt6.QtCore import QSize,QTime,QTimer,QUrl,Qt
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from messages import message_time_out,message_win,retourner_au_menu
import sys,os, random, copy, json



from data import update_joueur,get_joueur


class Piozla_level3(QFrame):
    def __init__(self, checkbox_state, parent):
        super().__init__()
        self.setFixedSize(1150,800)

        self.titre = QLabel("Piozla_level3", self)
        self.titre.setStyleSheet("color: White; font-size: 20px;")

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.parent = parent

        # charger la police
        QFontDatabase.addApplicationFont("./fonts/Digital-7 Mono.ttf")

        # son
        self.son = QAudioOutput()
        self.son2 =QAudioOutput()
        self.son3 = QAudioOutput()
        self.son_ooh  =QAudioOutput()
        self.son_win = QAudioOutput()
        self.son_shuffle = QAudioOutput()
        self.son_add_time = QAudioOutput()
        self.son_add_step = QAudioOutput()
        self.son_extra_bonus = QAudioOutput()
        self.son_erreur = QAudioOutput()
        self.son_timeless = QAudioOutput()



        # etat volume
        self.volume_state = checkbox_state

        if self.volume_state:
            self.parent.ajuster_volume(0.1)
            self.son.setVolume(1)
            self.son2.setVolume(1)
            self.son3.setVolume(1)
            self.son_ooh.setVolume(1)
            self.son_win.setVolume(1)
            self.son_extra_bonus.setVolume(1)
            self.son_add_step.setVolume(1)
            self.son_add_time.setVolume(1)
            self.son_shuffle.setVolume(1)
            self.son_erreur.setVolume(1)
            self.son_timeless.setVolume(1)
            print("son active")
        else:
            self.parent.ajuster_volume(0.0)
            self.son.setVolume(0.0)
            self.son2.setVolume(0.0)
            self.son3.setVolume(0.0)
            self.son_ooh.setVolume(0)
            self.son_win.setVolume(0)
            self.son_extra_bonus.setVolume(0)
            self.son_add_step.setVolume(0)
            self.son_add_time.setVolume(0)
            self.son_shuffle.setVolume(0)
            self.son_erreur.setVolume(0)
            self.son_timeless.setVolume(0)

            print("son desactive")



      

        # # fond-image
        # # image du fond
        img_fond = QPixmap("./images/png/tissus/taquin4.png")
        label_img_fond = QLabel(self)
        label_img_fond.setGeometry(450,50,600,660)
        label_img_fond.setScaledContents(True)
        taille_img_font = img_fond.scaled(800,800,Qt.AspectRatioMode.KeepAspectRatio)
        label_img_fond.setPixmap(taille_img_font)


        # initcson

        self.clack = QMediaPlayer()
        self.clack.setAudioOutput(self.son)
        self.clack.setSource(QUrl.fromLocalFile("./audio/MECHClik_Thermostat 1 (ID 2191)_LS.wav"))


        self.clack_back = QMediaPlayer()
        self.clack_back.setAudioOutput(self.son2)
        self.clack_back.setSource(QUrl.fromLocalFile("./audio/MECHClik_Thermostat 1 (ID 2191)_LS.wav"))

        self.clack_back_prec = QMediaPlayer()
        self.clack_back_prec.setAudioOutput(self.son3)
        self.clack_back_prec.setSource(QUrl.fromLocalFile("./audio/MECHClik_Thermostat 1 (ID 2191)_LS.wav"))


        self.audio_ooh = QMediaPlayer()
        self.audio_ooh.setAudioOutput(self.son_ooh)
        self.audio_ooh.setSource(QUrl.fromLocalFile("./audio/ooh-123103.mp3"))

        self.win = QMediaPlayer()
        self.win.setAudioOutput(self.son_win)
        self.win.setSource(QUrl.fromLocalFile("./audio/yay-6326.mp3"))

        self.audio_add_time = QMediaPlayer()
        self.audio_add_time.setAudioOutput(self.son_add_time)
        self.audio_add_time.setSource(QUrl.fromLocalFile("./audio/glass-break-316720.mp3"))

        self.audio_add_step = QMediaPlayer()
        self.audio_add_step.setAudioOutput(self.son_add_step)
        self.audio_add_step.setSource(QUrl.fromLocalFile("./audio/slide-whistle-up-326154.mp3"))

        self.audio_shuffle = QMediaPlayer()
        self.audio_shuffle.setAudioOutput(self.son_shuffle)
        self.audio_shuffle.setSource(QUrl.fromLocalFile("./audio//MECHHydr_Verin pneumatique petit 3 (ID 1493)_LS.wav"))

        self.audio_extra = QMediaPlayer()
        self.audio_extra.setAudioOutput(self.son_extra_bonus)
        self.audio_extra.setSource(QUrl.fromLocalFile("./audio/explosion-42132.mp3"))


        self.audio_erreur = QMediaPlayer()
        self.audio_erreur.setAudioOutput(self.son_erreur)
        self.audio_erreur.setSource(QUrl.fromLocalFile("./audio/error_sound-221445.mp3"))

        self.audio_timeless = QMediaPlayer()
        self.audio_timeless.setAudioOutput(self.son_timeless)
        self.audio_timeless.setSource(QUrl.fromLocalFile("./audio/clock-clock-sound-clock-clock-time-10343.mp3"))



        # nbr pas_init
        self.step = 0

        # timer
        # Timer
        self.duree_total = QTime(0,10,0)
        self.temps_restant = self.duree_total
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)
        self.timer_en_cours =False
       



    
        self.img_size = 300
        self.grid_size = 5

        # choisir une image aleatoirement
        self.img_path = self.choisir_img_hasard()

        # definir l'etat final du puzzle
        self.goal_state = list(range(1, 25)) + [0],
        
            
        self.board = self.shuffle()
        self.history = []
        self.future = []

        # decoupe l'image en tuiles
        self.tiles = self.slice_image()



        '''PARTIE GAUCHE'''
# fenetre a gauche
        self.win_gauche = QFrame(self)
        self.win_gauche.setGeometry(0,0,350,800)
        self.win_gauche.setStyleSheet("""
                                        background-image: url(./images/png/tissus/tissu2.webp);
                                      """)

        # btn_retour au menu
        self.btn_retour = QPushButton(self.win_gauche)
        self.btn_retour.setGeometry(10,50,50,50)
        self.btn_retour.setIcon(QIcon("./images/png/return.webp"))
        self.btn_retour.setStyleSheet("border-radius: 50px;")
        self.btn_retour.setIconSize(QSize(50,50))

        # connexion btn_retour
        self.btn_retour.clicked.connect(self.aller_au_menu)
    
        # label_level_jeu
        self.label_level = QLabel("Level 3", self.win_gauche)
        self.label_level.setGeometry(100,50,150,50)
        self.label_level.setStyleSheet("color: white; font-size: 50px;")

        # img originale
        self.label_img_original = QLabel(self.win_gauche)
        self.label_img_original.setGeometry(50,200,250,250)
        self.label_img_original.setPixmap(QPixmap(self.img_path).scaled(250,250))
        self.label_img_original.setStyleSheet("background-color: black; border: 2px solid black; border-radius: 5px;")

        # timer
        self.label_timer = QLabel(self.win_gauche)
        self.label_timer.setGeometry(65,630,250,100)
        self.label_timer.setText(f"{self.temps_restant.toString("hh:mm:ss")}")
        self.label_timer.setStyleSheet("""
                            background-color: black;
                            color:white;
                            font-size: 45px;
                            font-weight: bold;
                            font-family: 'Digital-7 Mono', 'Courier New', monospace;
                            """)
        
        # photo timer
        img_chrono = QPixmap("./images/png/btn/chrono1.png")
        label_img_chrono = QLabel(self)
        label_img_chrono.setGeometry(10,590,330,170)
        label_img_chrono.setScaledContents(True)
        taille_img_chrono = img_chrono.scaled(330,160,Qt.AspectRatioMode.KeepAspectRatio)
        label_img_chrono.setPixmap(taille_img_chrono)

        # nbr_pas
        self.nbr_pas = QLabel("0",self.win_gauche)
        self.nbr_pas.setGeometry(50,500,250,100)
        self.nbr_pas.setStyleSheet("""
                    
                    color: white;
                    font-size: 80px;
                    font-weight: bold;
                    font-family: 'Digital-7', 'Courier New', monospace;
                """)




        '''PARTIE DROITE'''
# plateau du jeu a droite
 
        self.plateau_puzzle = QFrame(self)
        self.plateau_puzzle.setGeometry(500,150,500,500)
        self.plateau_puzzle.setStyleSheet("""
                                        background-image: url(./images/png/carre4.png);
                                        background-repeat: no-repeat;
                                        background-position: center;
                                        border: 3px solid black;
                                        border-radius: 5px;

                                          """)

        self.grid_layout = QGridLayout(self.plateau_puzzle)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(5,5,5,5)

        self.buttons = [[None for _ in range(5)] for _ in range(5)]
        self.draw_board()

        # btn revenir en arriere
        self.btn_revenir_ = QPushButton(self)
        self.btn_revenir_.setGeometry(350,300,100,100)
        self.btn_revenir_.setIcon(QIcon("./images/png/btn/arriere1.png"))
        self.btn_revenir_.setStyleSheet("background-color: transparent;")
        self.btn_revenir_.setIconSize(QSize(100,100))
        self.btn_revenir_.clicked.connect(self.back)

        # btn aller en avant
        self.btn_aller_ = QPushButton(self)
        self.btn_aller_.setGeometry(350,400,100,100)
        self.btn_aller_.setIcon(QIcon("./images/png/btn/avant1.png"))
        self.btn_aller_.setStyleSheet("background-color: transparent;")

        self.btn_aller_.setIconSize(QSize(100,100))
        self.btn_aller_.clicked.connect(self.prec_)

        # desactivation bouton aller - retour
        self.btn_revenir_.setEnabled(False)
        self.btn_aller_.setEnabled(False)

        # btn_melanger le plateau
        self.btn_melanger = QPushButton("Melanger",self)
        self.btn_melanger.setGeometry(650,100,200,50)
        self.btn_melanger.clicked.connect(self.reshuffle)
        self.btn_melanger.setStyleSheet("background-color: rgb(45, 77, 142); color: white; font-size: 30px; border-radius: 15px; font-family: 'Digital-7', 'Courier New', monospace;font-weight: bold;")
       

        # label pack
        self.pack =QLabel(self)
        self.pack.setGeometry(620,720,270,60)
        self.pack.setStyleSheet("background-color: black; border-radius: 5px")
        self.pack.setCursor(Qt.CursorShape.PointingHandCursor)

        # add_time
        self.add_temps = QPushButton(self.pack)
        self.add_temps.setGeometry(5,5,50,50)
        self.add_temps.setIcon(QIcon("./images/png/kit/timeadd1.png"))
        self.add_temps.setIconSize(QSize(50,50))
        self.add_temps.clicked.connect(lambda: self.utiliser_bonus("add_temps"))
        self.add_temps.setEnabled(False)

        # - pas
        self.dim_nbr_pas = QPushButton(self.pack)
        self.dim_nbr_pas.setGeometry(75,5,50,50)
        self.dim_nbr_pas.setIcon(QIcon("./images/png/kit/pas.png"))
        self.dim_nbr_pas.setIconSize(QSize(50,50))
        self.dim_nbr_pas.clicked.connect(lambda: self.utiliser_bonus("dim_nbr_pas"))
        self.dim_nbr_pas.setEnabled(False)

          # activer_ btn_melanger
        self.activer_btn_melanger = QPushButton(self.pack)
        self.activer_btn_melanger.setGeometry(145,5,50,50)
        self.activer_btn_melanger.setIcon(QIcon("./images/png/kit/break11.png"))
        self.activer_btn_melanger.setIconSize(QSize(50,50))
        self.activer_btn_melanger.clicked.connect(lambda: self.utiliser_bonus("shuffle"))
        self.activer_btn_melanger.setEnabled(False)
        
          # activer_ btn_melanger
        self.special = QPushButton(self.pack)
        self.special.setGeometry(215,5,50,50)
        self.special.setIcon(QIcon("./images/png/kit/magicAs.jpeg"))
        self.special.setIconSize(QSize(50,50))
        self.special.clicked.connect(lambda: self.utiliser_bonus("special"))
        self.special.setEnabled(False)

        # label pour afficher la nombre de bonus
                # Ajouter un QLabel pour afficher le nombre associé à add_temps
        self.label_add_temps = QLabel("0", self.pack)
        self.label_add_temps.setGeometry(15, 5, 20, 20)  # Positionner au-dessus du bouton
        self.label_add_temps.setStyleSheet("""
            background-color: red;
            color: white;
            font-size: 12px;
            font-weight: bold;
            border-radius: 10px;
            border: 1px solid black;
            text-align: center;
        """)
        self.label_add_temps.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajouter un QLabel pour dim_nbr_pas
        self.label_dim_nbr_pas = QLabel("0", self.pack)
        self.label_dim_nbr_pas.setGeometry(85, 5, 20, 20)  # Positionner au-dessus du bouton
        self.label_dim_nbr_pas.setStyleSheet("""
            background-color: red;
            color: white;
            font-size: 12px;
            font-weight: bold;
            border-radius: 10px;
            border: 1px solid black;
            text-align: center;
        """)
        self.label_dim_nbr_pas.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajouter un QLabel pour activer_btn_shuffle
        self.label_activer_btn_shuffle = QLabel("0", self.pack)
        self.label_activer_btn_shuffle.setGeometry(155, 5, 20, 20)  # Positionner au-dessus du bouton
        self.label_activer_btn_shuffle.setStyleSheet("""
            background-color: red;
            color: white;
            font-size: 12px;
            font-weight: bold;
            border-radius: 10px;
            border: 1px solid black;
            text-align: center;
        """)
        self.label_activer_btn_shuffle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajouter un QLabel pour special
        self.label_special = QLabel("0", self.pack)
        self.label_special.setGeometry(225, 5, 20, 20)  # Positionner au-dessus du bouton
        self.label_special.setStyleSheet("""
            background-color: red;
            color: white;
            font-size: 12px;
            font-weight: bold;
            border-radius: 10px;
            border: 1px solid black;
            text-align: center;
        """)
        self.label_special.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # recuperation des donnees
        joueur = get_joueur()
        if joueur:
            _, _, _, _, add_temps_count, dim_nbr_pas_count, shuffle_count, special_count = joueur
            self.update_labels(add_temps_count, dim_nbr_pas_count, shuffle_count, special_count)
       




    # aller au menu
    def aller_au_menu(self):
        if retourner_au_menu(self):
            self.update_score()
            self.timer.stop()
            self.close()
            from piozla import Piozla
            self.win_menu = Piozla()
            self.win_menu.volume_check.setChecked(self.volume_state)
            self.win_menu.show()
        else:
            return
        
    def update_score(self):
    # Récupérer les données du joueur
        joueur = get_joueur()

        if joueur is None:
            QMessageBox.warning(self, "Erreur", "Aucun joueur trouvé dans la base de données.")
            return

        # Extraire les données du joueur
        joueur_id, temps, nb_pas, argent, add_temps_count, dim_nbr_pas_count, shuffle_count, special_count = joueur

        # Calculer le temps gagné
        duree_total = self.duree_total.hour() * 3600 + self.duree_total.minute() * 60 + self.duree_total.second()
        temps_restant = self.temps_restant.hour() * 3600 + self.temps_restant.minute() * 60 + self.temps_restant.second()
        temps_gagne = duree_total - temps_restant

        # Calculer l'argent gagné
        if self.step <= 60:
            argent_gagne = 300
        elif self.step <= 90:
            argent_gagne = 100
        elif self.step <= 120:
            argent_gagne = 50
        else :
            argent_gagne = 50

        if temps_gagne <= 0:
            argent_gagne -= 200
        elif temps_gagne  >= duree_total//2:
            argent_gagne += 100
        else:
            argent_gagne += 200

        argent += argent_gagne

        # Mettre à jour les données du joueur
        print(temps_gagne, self.step, argent, add_temps_count, dim_nbr_pas_count, shuffle_count, special_count)
        update_joueur(temps_gagne, self.step, argent, add_temps_count, dim_nbr_pas_count, shuffle_count, special_count)
            
    # bonus 
    #  
    def utiliser_bonus(self, bonus_type):
    # Récupérer les données du joueur
        joueur = get_joueur()
        if joueur is None:
            QMessageBox.warning(self, "Erreur", "Aucun joueur trouvé dans la base de données.")
            return

        joueur_id, temps, nb_pas, argent, add_temps_count, dim_nbr_pas_count, shuffle_count, special_count = joueur

        # Décrémenter le bonus correspondant
        if bonus_type == "add_temps" and add_temps_count > 0:
            add_temps_count -= 1
            self.audio_timeless.stop()
            self.audio_add_time.play()
            self.temps_restant = self.temps_restant.addSecs(+30)  # Ajouter 30 secondes
            print("Temps ajouté : +30 secondes")
            self.label_timer.setStyleSheet("""
                            background-color: black;
                            color:gold;
                            font-size: 45px;
                            font-weight: bold;
                            font-family: 'Digital-7 Mono', 'Courier New', monospace;
                            """)
        elif bonus_type == "dim_nbr_pas" and dim_nbr_pas_count > 0:
            dim_nbr_pas_count -= 1
            self.audio_add_step.play()
            self.step -= 5  # Réduire le nombre de pas
            self.nbr_pas.setText(f"{self.step}🎇")
            print("Nombre de pas réduit de 5")
        elif bonus_type == "shuffle" and shuffle_count > 0:
            shuffle_count -= 1
            self.audio_shuffle.play()
            self.reshuffle()
            self.btn_melanger.setEnabled(True)  # Activer le mélange
            print("Mélange activé")
        elif bonus_type == "special" and special_count > 0:
            special_count -= 1
            self.audio_timeless.stop()
            self.audio_extra.play()
            self.temps_restant = self.temps_restant.addSecs(+120)
            self.label_timer.setStyleSheet("""
                            background-color: black;
                            color:gold;
                            font-size: 45px;
                            font-weight: bold;
                            font-family: 'Digital-7 Mono', 'Courier New', monospace;
                            """)  
            
            self.label_timer.setText(f"{self.temps_restant.toString("hh:mm:ss")}")
            self.step -= 20
            self.nbr_pas.setText(f"{self.step}🎇")
            print("Pouvoir spécial activé")
        else:
            self.audio_erreur.play()
            # Désactiver le bouton correspondant
            if bonus_type == "add_temps":
                self.add_temps.setEnabled(False)
            elif bonus_type == "dim_nbr_pas":
                self.dim_nbr_pas.setEnabled(False)
            elif bonus_type == "shuffle":
                self.activer_btn_melanger.setEnabled(False)
            elif bonus_type == "special":
                self.special.setEnabled(False)
            return 

    # Mettre à jour la base de données
        update_joueur(temps, nb_pas, argent, add_temps_count, dim_nbr_pas_count, shuffle_count, special_count)

        # Mettre à jour les labels
        self.update_labels(add_temps_count, dim_nbr_pas_count, shuffle_count, special_count)

    def update_labels(self, add_temps_count, dim_nbr_pas_count, shuffle_count, special_count):
        self.label_add_temps.setText(str(add_temps_count))
        self.label_dim_nbr_pas.setText(str(dim_nbr_pas_count))
        self.label_activer_btn_shuffle.setText(str(shuffle_count))
        self.label_special.setText(str(special_count))

    def choisir_img_hasard(self):
        dossier_img = 'images'
        fichiers = [
            f for f in os.listdir(dossier_img)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]
        if not fichiers:
            raise FileNotFoundError("Aucune image trouve dans dossier images")
        return os.path.join(dossier_img, random.choice(fichiers))
    
    
    
        # melanger
    def shuffle(self):
        nums = list(range(25))
        while True:
            random.shuffle(nums)
            if self.is_solvable(nums):
                return [nums[i:i + 5] for i in range(0, 25, 5)]
            
    def is_solvable(self, nums):
        inv_count = sum(
            1 for i in range(len(nums)) for j in range(i + 1, len(nums))
            if nums[i] != 0 and nums[i] > nums[j]
        )
        return inv_count %2 == 0
    

    # couper l'image en morceaux
    def slice_image(self):
        pixmap = QPixmap(self.img_path).scaled(600,600)
        w= 600//5
        tiles = {}
        counter = 1
        for i in range(5):
            for j in range(5):
                if counter == 25:
                    tiles[0] = None
                    break
                tile = pixmap.copy(j * w, i * w, w,w).scaled(w,w)
                tiles[counter] = tile
                counter += 1
        return tiles
    
    def draw_board(self):
        frame_width = self.plateau_puzzle.width()
        frame_height = self.plateau_puzzle.height()

        # btn taille
        btn_width = (frame_width - 40) // 5
        btn_height = (frame_height - 40) // 5

        for i in range(5):
            for j in range(5):
                value = self.board[i][j]
                btn = QPushButton()
                btn.setFixedSize(btn_width, btn_height)
                if value != 0:
                    icon = QIcon(self.tiles[value])
                    btn.setIcon(icon)
                    btn.setIconSize(QSize(btn_width - 8, btn_height - 8))
                    btn.setStyleSheet(" border: 3px solid rgb(61, 61, 61);box-shadow: 50px 50px 100px rgba(0,0,0,0.5);")
                else:
                    btn.setIcon(QIcon("./images/png/tissus/vide.png"))
                    btn.setIconSize(QSize(btn_width, btn_width))
                    btn.setStyleSheet(" border: 3px solid rgb(61, 61, 61);box-shadow: 50px 50px 100px rgba(0,0,0,0.5);")
                btn.clicked.connect(lambda _, x= i, y = j:self.try_move(x,y))
                self.grid_layout.addWidget(btn, i, j)
                self.buttons[i][j] = btn

   
   

    

    def update_timer(self):
        self.temps_restant = self.temps_restant.addSecs(-1)
        self.label_timer.setText(f"{self.temps_restant.toString("hh:mm:ss")}")

        if self.temps_restant == QTime(0,0,10):
            self.audio_timeless.play()
            self.label_timer.setStyleSheet("""
                            background-color: black;
                            color:red;
                            font-size: 45px;
                            font-weight: bold;
                            font-family: 'Digital-7 Mono', 'Courier New', monospace;
                            """)

        if self.temps_restant == QTime(0,0,0):
            
        # mis a jours du joueur 
            # self.update_score()

            self.timer.stop()
            self.audio_ooh.play()
            message_time_out(parent=self)
            self.desactiver_puzzle()

    def desactiver_puzzle(self):
        self.enregistrer_score_si_meilleur()
        for i in range(5):
            for j in range(5):
                self.buttons[i][j].setEnabled(False)
                self.btn_revenir_.setEnabled(False)
                self.btn_aller_.setEnabled(False)
                self.btn_melanger.setEnabled(True)
                self.btn_melanger.setStyleSheet("background-color: rgb(45, 77, 142); color: white; font-size: 30px; border-radius: 15px; font-family: 'Digital-7', 'Courier New', monospace;font-weight: bold;")
                self.btn_melanger.setText("Rejouer")
                self.add_temps.setEnabled(False)
                self.dim_nbr_pas.setEnabled(False)
                self.activer_btn_melanger.setEnabled(False)
                self.special.setEnabled(False)
                self.label_timer.setStyleSheet("""
                            background-color: black;
                            color:white;
                            font-size: 45px;
                            font-weight: bold;
                            font-family: 'Digital-7 Mono', 'Courier New', monospace;
                            """)
                self.temps_restant = QTime(0,10,0)
                self.label_timer.setText(f"{self.temps_restant.toString("hh:mm:ss")}")
                self.step = 0
                self.nbr_pas.setText(f"{self.step}")
                self.timer_en_cours = False
                
                


    def find_empty(self):
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 0:
                    return i, j
            
                
    def try_move(self, i,j):  
        empty_i , empty_j = self.find_empty()
        if abs(empty_i - i) + abs(empty_j - j)== 1:
            if not self.timer_en_cours:
                self.timer.start()
                self.timer_en_cours =True

            self.history.append(copy.deepcopy(self.board))
            self.future.clear()
            self.board[empty_i][empty_j], self.board[i][j] = self.board[i][j], self.board[empty_i][empty_j]
            self.clack.play()
            self.update_board()
            self.step += 1
            self.nbr_pas.setText(f"{self.step}")
            self.btn_melanger.setStyleSheet("background-color: gray; color: white; font-size: 30px; border-radius: 15px; font-family: 'Digital-7', 'Courier New', monospace;font-weight: bold;")
            self.btn_melanger.setEnabled(False)
            self.add_temps.setEnabled(True)
            self.dim_nbr_pas.setEnabled(True)
            self.activer_btn_melanger.setEnabled(True)
            self.special.setEnabled(True)
            self.btn_revenir_.setEnabled(True)
            self.btn_aller_.setEnabled(True)

            if self.is_solved():
                self.timer.stop()
                self.update_score()
                message_win(parent=self)
                self.win.play()
                self.desactiver_puzzle()

                self.parent.aller_niveau_suivant("Expert")

    
    
    # si c'est resolu
    def is_solved(self):
        flat = [num for row in self.board for num in row]
        numbers_without_zero = [n for n in flat if n != 0]
        return numbers_without_zero == list(range(1, 16))

    

    def back(self):
        if self.history:
            self.future.append(copy.deepcopy(self.board))
            self.clack_back.play()
            self.board  = self.history.pop()
            self.update_board()
            self.btn_aller_.setEnabled(True)
        else:
            self.audio_erreur.play()
            self.btn_revenir_.setEnabled(False)
        

    def prec_(self):
        if self.future:
            self.history.append(copy.deepcopy(self.board))
            self.clack_back_prec.play()
            self.board = self.future.pop()
            self.update_board()
            self.btn_revenir_.setEnabled(True)
        else:
            self.audio_erreur.play()
            self.btn_aller_.setEnabled(False)

    def reshuffle(self):
        self.audio_shuffle.play()
        self.board = self.shuffle()
        self.history.clear()
        self.future.clear()
        self.update_board()
        self.btn_melanger.setStyleSheet("background-color: rgb(45, 77, 142); color: white; font-size: 30px; border-radius: 15px; font-family: 'Digital-7', 'Courier New', monospace;font-weight: bold;")
        self.btn_melanger.setText("Melanger")
        for i in range(5):
            for j in range(5):
                self.buttons[i][j].setEnabled(True)
                self.btn_revenir_.setEnabled(False)
                self.btn_aller_.setEnabled(False)


    def update_board(self):
        frame_width = self.plateau_puzzle.width()
        frame_height = self.plateau_puzzle.height()

        # btn taille
        btn_width = (frame_width - 40) // 5
        btn_height = (frame_height - 40) // 5

        for i in range(5):
            for j in range(5):
                value = self.board[i][j]
                btn = self.buttons[i][j]
                if value != 0 :
                    icon = QIcon(self.tiles[value])
                    btn.setIcon(icon)
                    btn.setIconSize(QSize(btn_width - 7,btn_height -7))
                    btn.setStyleSheet(" border: 3px solid rgb(61, 61, 61);box-shadow: 50px 50px 100px rgba(0,0,0,0.5);")

                else:
                    btn.setIcon(QIcon("./images/png/tissus/vide.png"))
                    btn.setStyleSheet(" border: 3px solid rgb(61, 61, 61);box-shadow: 50px 50px 100px rgba(0,0,0,0.5);")
                

  

    def enregistrer_score_si_meilleur(self):
        score = {
            'pas' :self.step,
            'temps': self.temps_restant.toString("hh:mm:ss")
        }

        if os.path.exists("score.json"):
            with open("score.js", "r") as f:
                meilleur = json.load(f)

                # comparaison
                meilleur_pas = meilleur.get("pas", float("inf"))
                meilleur_temps = QTime.fromString(meilleur.get("temps", "99:59:59")),

                if (self.step < meilleur_pas) or (self.step == meilleur_pas and self.temps_restant > meilleur_temps):
                    with open("score.json", "w") as f:
                        json.dump(score, f)
                    print(f"Nouveau score: {meilleur_pas},{meilleur_temps}")


        else:
            with open("json", "w") as f:
                json.dump(score, f)
            print(f"premier score: {self.step, self.temps_restant}")


       
  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win  = Piozla_level3()
    win.show()
    sys.exit(app.exec())