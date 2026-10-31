import tkinter as tk
from tkinter import ttk, messagebox

from manteniment.alta_pacient import validar_dni_nie


def registrar_personal(conn,nom, cognoms, dni, adreca, telefon,
                       rol, especialitat, curriculum, id_metge):

    try:
        cur = conn.cursor()

        # 🔑 PAS 1: Inserir a PERSONAL i recuperar l'ID autogenerat
        cur.execute("""
            INSERT INTO PERSONAL (nom, cognoms, dni, adreca, telefon)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_personal
        """, (nom, cognoms, dni, adreca, telefon))
        
        # Obtenir l'ID que acaba de generar la BBDD
        id_personal = cur.fetchone()[0]
       
        if rol == "Metge":
            cur.execute("""
                INSERT INTO METGE (id_personal, especialitat_metge, dades_curriculum_metge)
                VALUES (%s, %s, %s)
            """, (id_personal, especialitat, curriculum))

        elif rol == "Infermer/a":
            cur.execute("""
                INSERT INTO INFERMERIA (id_personal, especialitat_infermeria,
                dades_curriculum_infermera, id_metge)
                VALUES (%s, %s, %s, %s)
            """, ( id_personal,especialitat, curriculum, id_metge))

        elif rol == "Personal de neteja" or rol == "Administratiu":
            cur.execute("""
                INSERT INTO VARI (id_personal,tipus_tasca)
                VALUES (%s,%s)
            """, ( id_personal,rol))

        conn.commit()
        cur.close()

        messagebox.showinfo("Correcte", "Personal registrat correctament")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def finestra_alta_personal(conn):
    root = tk.Toplevel()
    root.title("Alta de Personal (ADMIN)")
    root.geometry("400x600")



    # Nom
    tk.Label(root, text="Nom").pack()
    entry_nom = tk.Entry(root)
    entry_nom.pack()

    # Cognoms
    tk.Label(root, text="Cognoms").pack()
    entry_cognoms = tk.Entry(root)
    entry_cognoms.pack()

    # DNI
    tk.Label(root, text="DNI").pack()
    entry_dni = tk.Entry(root)
    entry_dni.pack()

    # Adreça
    tk.Label(root, text="Adreça").pack()
    entry_adreca = tk.Entry(root)
    entry_adreca.pack()

    # Telèfon
    tk.Label(root, text="Telèfon").pack()
    entry_telefon = tk.Entry(root)
    entry_telefon.pack()

    # Rol
    tk.Label(root, text="Rol").pack()
    combo_rol = ttk.Combobox(root, values=["Metge", "Infermer/a", "Personal de neteja","Administratiu"])
    combo_rol.pack()

    # Especialitat
    tk.Label(root, text="Especialitat (si aplica)").pack()
    entry_especialitat = tk.Entry(root)
    entry_especialitat.pack()

    # Curriculum
    tk.Label(root, text="Curriculum (si aplica)").pack()
    entry_curriculum = tk.Entry(root)
    entry_curriculum.pack()

    # ID Metge
    tk.Label(root, text="ID Metge responsable (només infermeria)").pack()
    entry_id_metge = tk.Entry(root)
    entry_id_metge.pack()

    # BOTÓ GUARDAR
    def guardar():
        nom = entry_nom.get()
        cognoms = entry_cognoms.get()
        dni = entry_dni.get()
        adreca = entry_adreca.get()
        telefon = entry_telefon.get()
        rol = combo_rol.get()
        especialitat = entry_especialitat.get()
        curriculum = entry_curriculum.get()
        id_metge = entry_id_metge.get() if rol == "Infermer/a" else None

        if not validar_dni_nie(dni):
            messagebox.showerror("Error", "DNI o NIE no vàlid")
            return

        registrar_personal(conn,
             nom, cognoms, dni, adreca, telefon,
            rol, especialitat, curriculum, id_metge)
        
        root.destroy()

    tk.Button(root, text="Guardar", command=guardar).pack(pady=15)

    root.mainloop()


