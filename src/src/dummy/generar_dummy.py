# dummy/generar_dummy.py
from faker import Faker
import random
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

import psycopg2

conn = psycopg2.connect(
    host="192.168.56.103",
    database="hospital",
    user="postgres",
    password="1234"
)


fake = Faker('es_ES')
fake_cirillic = Faker('ru_RU')

def generar_todo():
    """Funció principal que genera totes les dades dummy"""
    
    root = tk.Tk()
    root.withdraw()
    
    result = messagebox.askyesno(
        "Confirmar",
        "Això generarà desenes de milers de registres.\n"
        "Pot trigar diversos minuts.\n\n"
        "Vols continuar?"
    )
    
    if not result:
        root.destroy()
        return
    
    root.destroy()
    

    
    try:
        conn.autocommit = False
        cur = conn.cursor()
        
        print("Iniciant generació de dades...")
        
        # 1. Crear plantes
        crear_plantes(cur)
        print(" Plantes creades")
        
        # 2. Crear habitacions
        crear_habitacions(cur)
        print(" Habitacions creades")
        
        # 3. Crear tipus d'aparells
        crear_tipus_aparells(cur)
        print("Tipus d'aparells creats")
        
        # 4. Crear aparells mèdics
        crear_aparells_medics(cur)
        print("Aparells mèdics creats")
        
        # 5. Crear quiròfans
        crear_quirofans(cur)
        print("Quiròfans creats")
        
        # 6. Assignar aparells a quiròfans
        assignar_aparells_a_quirofans(cur)
        print("Aparells assignats a quiròfans")
        
        # 7. Crear personal (base)
        ids_personal = crear_personal(cur)
        print(f"Personal creat: {len(ids_personal)} registres")
        
        # 8. Crear metges
        ids_metge = crear_metges(cur, ids_personal[:100])
        print(f"Metges creats: {len(ids_metge)}")
        
        # 9. Crear infermeres
        ids_infermera = crear_infermeres(cur, ids_personal[100:300], ids_metge)
        print(f"Infermeres creades: {len(ids_infermera)}")
        
        # 10. Crear personal vari
        ids_vari = crear_personal_vari(cur, ids_personal[300:450])
        print(f"Personal vari creat: {len(ids_vari)}")
        
        # 11. Crear pacients
        ids_pacient = crear_pacients(cur)
        print(f"Pacients creats: {len(ids_pacient)}")
        
        # 12. Crear horaris per metges
        crear_horaris_metges(cur, ids_metge)
        print("Horaris creats")
        
        # 13. Crear visites
        crear_visites(cur, ids_pacient, ids_metge)
        print("Visites creades")
        
        # 14. Crear medicaments i receptes
        crear_medicaments_i_receptes(cur)
        print("Medicaments i receptes creats")
        
        # 15. Crear operacions
        crear_operacions(cur, ids_pacient, ids_metge)
        print("Operacions creades")
        
        # 16. Crear assistència a operacions
        crear_assistencia_operacions(cur)
        print("Assistència a operacions creada")
        
        # 17. Crear reserves d'habitacions
        crear_reserves_habitacions(cur, ids_pacient)
        print("Reserves d'habitacions creades")
        
        conn.commit()
        
        messagebox.showinfo("Èxit", "Dades dummy generades correctament!")
        print("Procés completat amb èxit!")
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Error", f"Error al generar dades:\n{str(e)}")
        print(f" ERROR: {e}")



def crear_plantes(cur):
    """Crea les 4 plantes"""
    for num_planta in range(1, 5):
        cur.execute("""
            INSERT INTO planta (num_planta) VALUES (%s) ON CONFLICT (num_planta) DO NOTHING
        """, (num_planta,))


def crear_habitacions(cur):
    """Crea 20 habitacions per planta (total 80)"""
    id_habitacio = 1
    for planta in range(1, 5):
        for num_habitacio in range(1, 21):
            cur.execute("""
                INSERT INTO habitacio (id_habitacio, num_habitacio, num_planta)
                VALUES (%s, %s, %s) ON CONFLICT (id_habitacio) DO NOTHING
            """, (id_habitacio, num_habitacio, planta))
            id_habitacio += 1


def crear_tipus_aparells(cur):
    """Crea tipus d'aparells mèdics"""
    tipus = ['Respirador', 'Desfibril·lador', 'Monitor de signes', 'Màquina d\'oxigen', 'Electrocardiògraf']
    for nom_tipus in tipus:
        cur.execute("""
            INSERT INTO tipus_aparell (nom_tipus) VALUES (%s) ON CONFLICT (id_tipus) DO NOTHING
        """, (nom_tipus,))


def crear_aparells_medics(cur):
    """Crea aparells mèdics"""
    # Obtenir ids dels tipus
    cur.execute("SELECT id_tipus, nom_tipus FROM tipus_aparell")
    tipus = cur.fetchall()
    
    id_aparell = 1
    for _ in range(30):  # 30 aparells en total
        id_tipus = random.choice(tipus)[0]
        nom_aparell = f"{random.choice(['Philips', 'Siemens', 'GE', 'Medtronic'])} {fake.random_number(digits=3)}"
        
        cur.execute("""
            INSERT INTO aparell_medic (id_aparell, nom_aparell, id_tipus)
            VALUES (%s, %s, %s) ON CONFLICT (id_aparell) DO NOTHING
        """, (id_aparell, nom_aparell, id_tipus))
        id_aparell += 1


def crear_quirofans(cur):
    """Crea 2 quiròfans per planta (total 8) amb IDs Q1, Q2, Q3..."""

    id_num = 1
    for planta in range(1, 5):          # Plantas 1 a 4
        for num_quirofan in range(1, 3):  # Dos quiròfans por planta
            id_quirofan = f"Q{id_num}"    # Genera 
            
            cur.execute("""
                INSERT INTO quirofan (id_quirofan, num_quirofan, num_planta)
                VALUES (%s, %s, %s)
                ON CONFLICT (id_quirofan) DO NOTHING
            """, (id_quirofan, num_quirofan, planta))

            id_num += 1


def assignar_aparells_a_quirofans(cur):
    """Assigna aparells als quiròfans"""
    cur.execute("SELECT id_quirofan FROM quirofan")
    quirofans = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT id_aparell FROM aparell_medic")
    aparells = [row[0] for row in cur.fetchall()]
    
    for id_quirofan in quirofans:
        # Cada quiròfan té entre 5 i 10 aparells
        num_aparells = random.randint(5, 10)
        aparells_assignats = random.sample(aparells, min(num_aparells, len(aparells)))
        
        for id_aparell in aparells_assignats:
            quantitat = random.randint(1, 3)
            cur.execute("""
                INSERT INTO aparell_en_quirofan (id_quirofan, id_aparell, quantitat)
                VALUES (%s, %s, %s) ON CONFLICT (id_quirofan, id_aparell) DO NOTHING
            """, (id_quirofan, id_aparell, quantitat))


def crear_personal(cur):
    """Crea 450 persones (base per tothom)"""
    ids = []
    
    for i in range(450):
        if random.random() < 0.2:
            nom = fake_cirillic.first_name()
            cognoms = fake_cirillic.last_name() + " " + fake_cirillic.last_name()
        else:
            nom = fake.first_name()
            cognoms = fake.last_name() + " " + fake.last_name()
        
        dni = fake.unique.bothify('########?', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ').upper()
        adreca = fake.address()
        telefon = fake.phone_number()
        
        cur.execute("""
            INSERT INTO personal (nom, cognoms, dni, adreca, telefon)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_personal
        """, (nom, cognoms, dni, adreca, telefon))
        
        ids.append(cur.fetchone()[0])
    
    return ids


def crear_metges(cur, ids_personal):
    """Crea metges"""
    especialitats = ['Cardiologia', 'Pediatria', 'Traumatologia', 'Neurologia', 
                     'Oncologia', 'Dermatologia', 'Oftalmologia', 'Psiquiatria', 
                     'Ginecologia', 'Urologia']
    
    for id_personal in ids_personal:
        especialitat = random.choice(especialitats)
        curriculum = f"Llicenciat en Medicina, {random.randint(5, 30)} anys d'experiència."
        
        cur.execute("""
            INSERT INTO metge (id_personal, especialitat_metge, dades_curriculum_metge)
            VALUES (%s, %s, %s)
        """, (id_personal, especialitat, curriculum))
    
    return ids_personal


def crear_infermeres(cur, ids_personal, ids_metge):
    """Crea infermeres"""
    especialitats = ['Infermeria General', 'Pediatria', 'Quiròfan', 'Urgències', 'UCI']
    
    for id_personal in ids_personal:
        especialitat = random.choice(especialitats)
        curriculum = f"Diplomada en Infermeria, {random.randint(2, 20)} anys d'experiència."
        
        # 70% assignades a un metge, 30% de planta
        if random.random() < 0.7:
            id_metge = random.choice(ids_metge)
        else:
            id_metge = None
        
        id_planta = random.randint(1, 4)
        
        cur.execute("""
            INSERT INTO infermeria (id_personal, especialitat_infermeria, dades_curriculum_infermera, id_metge, id_planta)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_personal, especialitat, curriculum, id_metge, id_planta))
    
    return ids_personal


def crear_personal_vari(cur, ids_personal):
    """Crea personal vari (neteja i administratius)"""
    for i, id_personal in enumerate(ids_personal):
        if i < 100:  # Primeres 100 = neteja
            tipus = 'Neteja'
        else:  # Les 50 restants = administratius
            tipus = 'Administratiu'
        
        cur.execute("""
            INSERT INTO vari (id_personal, tipus_tasca)
            VALUES (%s, %s)
        """, (id_personal, tipus))
    
    return ids_personal


def crear_pacients(cur):
    """Crea 50.000 pacients"""
    ids = []
    
    for i in range(50000):
        if random.random() < 0.15:
            nom = fake_cirillic.first_name()
            cognoms = fake_cirillic.last_name() + " " + fake_cirillic.last_name()
        else:
            nom = fake.first_name()
            cognoms = fake.last_name() + " " + fake.last_name()
        
        dni = fake.unique.bothify('########?', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ').upper()
        adreca = fake.address()
        telefon = fake.phone_number()
        
        cur.execute("""
            INSERT INTO pacient (nom_pacient, cognoms_pacient, dni_pacient, adreca_pacient, telefon_pacient)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_pacient
        """, (nom, cognoms, dni, adreca, telefon))
        
        ids.append(cur.fetchone()[0])
        
        if (i + 1) % 5000 == 0:
            print(f"  {i+1}/50000 pacients...")
    
    return ids


def crear_horaris_metges(cur, ids_metge):
    """Crea horaris per metges (dilluns a divendres, 9-14h)"""
    dies = ['Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres']
    
    id_horari = 1
    for id_metge in ids_metge:
        dies_treball = random.sample(dies, random.randint(3, 5))
        
        for dia in dies_treball:
            cur.execute("""
                INSERT INTO horari_metge (id_horari, id_metge, dia_setmana, hora_inici, hora_fi)
                VALUES (%s, %s, %s, '09:00:00', '14:00:00')
            """, (id_horari, id_metge, dia))
            id_horari += 1


def crear_visites(cur, ids_pacient, ids_metge):
    """Crea 100.000 visites"""
    data_inici = datetime(2024, 1, 1)
    data_fi = datetime(2026, 5, 13)
    
    diagnostics = [
        "Refredat comú", "Grip", "Hipertensió arterial", "Diabetis tipus 2",
        "Fractura de radi", "Lumbàlgia", "Migranya", "Bronquitis aguda",
        "Al·lèrgia estacional", "Ansietat generalitzada", "Infecció d'orina", "Gastritis"
    ]
    
    id_visita = 1
    for i in range(100000):
        data = fake.date_between(start_date=data_inici, end_date=data_fi)
        hora = fake.time_object()
        diagnostic = random.choice(diagnostics)
        id_pacient = random.choice(ids_pacient)
        id_metge = random.choice(ids_metge)
        
        cur.execute("""
            INSERT INTO visita (id_visita, data, hora, diagnostic, id_pacient, id_metge)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_visita, data, hora, diagnostic, id_pacient, id_metge))
        
        id_visita += 1
        
        if (i + 1) % 10000 == 0:
            print(f"  {i+1}/100000 visites...")


def crear_medicaments_i_receptes(cur):
    """Crea medicaments i receptes associades a visites"""
    # Obtenir visites
    cur.execute("SELECT id_visita FROM visita")
    visites = [row[0] for row in cur.fetchall()]
    
    # Crear medicaments
    medicaments = [
        ("Paracetamol", "Analgèsic i antipirètic"),
        ("Ibuprofè", "Antiinflamatori no esteroidal"),
        ("Amoxicil·lina", "Antibiòtic de ampli espectre"),
        ("Omeprazole", "Inhibidor de la bomba de protons"),
        ("Atorvastatina", "Redueix el colesterol LDL"),
        ("Metformina", "Antidiabètic oral"),
        ("Lorazepam", "Ansiolític benzodiazepínic"),
        ("Salbutamol", "Broncodilatador per asma")
    ]
    
    ids_medicament = []
    id_medicament = 1
    for nom, desc in medicaments:
        cur.execute("""
            INSERT INTO medicament (id_medicament, nom_medicament, descripcio)
            VALUES (%s, %s, %s) ON CONFLICT (id_medicament) DO NOTHING RETURNING id_medicament
        """, (id_medicament, nom, desc))
        result = cur.fetchone()
        if result:
            ids_medicament.append(result[0])
        id_medicament += 1
    
    # Receptes per al 30% de les visites
    num_receptes = min(len(visites), 30000)
    visites_recepta = random.sample(visites, num_receptes)
    
    id_receptat = 1
    for i, id_visita in enumerate(visites_recepta):
        id_medicament = random.choice(ids_medicament)
        dosi = random.choice(['500mg', '1g', '250mg', '750mg'])
        frequencia = random.choice(['Cada 8 hores', 'Cada 12 hores', 'Cada 24 hores', 'Un cop al dia'])
        
        cur.execute("""
            INSERT INTO medicament_receptat (id_receptat, dosi, frequencia, id_visita, id_medicament)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_receptat, dosi, frequencia, id_visita, id_medicament))
        
        id_receptat += 1
        
        if (i + 1) % 5000 == 0:
            print(f"  {i+1}/{num_receptes} receptes...")


def crear_operacions(cur, ids_pacient, ids_metge):
    """Crea operacions per a un 5% dels pacients"""
    # Obtenir quiròfans
    cur.execute("SELECT id_quirofan FROM quirofan")
    quirofans = [row[0] for row in cur.fetchall()]
    
    if not quirofans:
        return
    
    num_operacions = min(len(ids_pacient), 2500)
    pacients_operats = random.sample(ids_pacient, num_operacions)
    
    id_operacio = 1
    for id_pacient in pacients_operats:
        data_operacio = fake.date_between(start_date='-2y', end_date='today')
        hora_operacio = fake.time_object()
        id_metge = random.choice(ids_metge)
        id_quirofan = random.choice(quirofans)
        
        cur.execute("""
            INSERT INTO operacio (id_operacio, data_operacio, hora_operacio, id_quirofan, id_metge, id_pacient)
            VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id_operacio) DO NOTHING
        """, (id_operacio, data_operacio, hora_operacio, id_quirofan, id_metge, id_pacient))
        
        id_operacio += 1


def crear_assistencia_operacions(cur):
    """Crea assistència d'infermeres a operacions"""
    # Obtenir operacions
    cur.execute("SELECT id_operacio FROM operacio")
    operacions = [row[0] for row in cur.fetchall()]
    
    # Obtenir infermeres
    cur.execute("SELECT id_personal FROM infermeria")
    infermeres = [row[0] for row in cur.fetchall()]
    
    for id_operacio in operacions:
        # Cada operació té entre 2 i 5 infermeres assistents
        num_assistents = random.randint(2, 5)
        assistents = random.sample(infermeres, min(num_assistents, len(infermeres)))
        
        for id_infermeria in assistents:
            cur.execute("""
                INSERT INTO assistencia_operacio (id_operacio, id_infermeria)
                VALUES (%s, %s) ON CONFLICT (id_operacio, id_infermeria) DO NOTHING
            """, (id_operacio, id_infermeria))


def crear_reserves_habitacions(cur, ids_pacient):
    """Crea reserves per al 10% dels pacients"""
    # Obtenir habitacions
    cur.execute("SELECT id_habitacio FROM habitacio")
    habitacions = [row[0] for row in cur.fetchall()]
    
    if not habitacions:
        return
    
    num_reserves = min(len(ids_pacient), 5000)
    pacients_reserva = random.sample(ids_pacient, num_reserves)
    
    id_reserva = 1
    for id_pacient in pacients_reserva:
        data_ingres = fake.date_between(start_date='-1y', end_date='today')
        data_sortida = data_ingres + timedelta(days=random.randint(1, 14))
        id_habitacio = random.choice(habitacions)
        
        cur.execute("""
            INSERT INTO reserva_habitacio (id_reserva, data_ingres_prevista, data_sortida_prevista, id_pacient, id_habitacio)
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id_reserva) DO NOTHING
        """, (id_reserva, data_ingres, data_sortida, id_pacient, id_habitacio))
        
        id_reserva += 1
