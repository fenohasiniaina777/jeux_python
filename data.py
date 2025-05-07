import sqlite3

# Création de la table joueur
conn = sqlite3.connect("base.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS joueur(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temps INTEGER DEFAULT 0,
        nb_pas INTEGER DEFAULT 0,
        argent INTEGER DEFAULT 15000,
        boite1 INTEGER DEFAULT 0,
        boite2 INTEGER DEFAULT 0,
        boite3 INTEGER DEFAULT 0,
        boite4 INTEGER DEFAULT 0
    )
""")
conn.commit()
conn.close()

def add_new_joueur():
    conn = sqlite3.connect("base.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO joueur (temps, nb_pas, argent) VALUES (0, 0, 15000)")
    conn.commit()
    conn.close()
    print("Joueur ajouté.")

def get_joueur():
    conn = sqlite3.connect("base.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM joueur LIMIT 1")
    joueur = cur.fetchone()
    
    if joueur is None:
        print("Aucun joueur trouvé. Création d'un joueur par défaut.")
        cur.execute("INSERT INTO joueur (temps, nb_pas, argent) VALUES (0, 0, 15000)")
        conn.commit()
        cur.execute("SELECT * FROM joueur LIMIT 1")
        joueur = cur.fetchone()

    conn.close()
    return joueur

def update_joueur(temps, nb_pas, argent, add_temps_count, dim_nbr_pas_count, shuffle_count, special_count):
    conn = sqlite3.connect("base.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE joueur
        SET temps = ?, nb_pas = ?, argent = ?, 
            boite1 = ?, boite2 = ?, boite3 = ?, boite4 = ?
        WHERE id = 1
    """, (temps, nb_pas, argent, add_temps_count, dim_nbr_pas_count, shuffle_count, special_count))
    conn.commit()
    conn.close()
    print("Joueur mis à jour avec succès.")

def update_boite(joueur_id, boite_index):
    conn = sqlite3.connect("base.db")
    cur = conn.cursor()

    # identifier la colonne_boite
    colonne_boite = f"boite{boite_index + 1}"
    cur.execute(f"UPDATE joueur SET {colonne_boite} = {colonne_boite} + 1 WHERE id = ?", (joueur_id,))
    conn.commit()
    conn.close()
    print(f"Boîte {boite_index + 1} mise à jour pour le joueur {joueur_id}.")