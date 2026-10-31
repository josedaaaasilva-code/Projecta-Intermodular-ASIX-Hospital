import tkinter as tk
from tkinter import messagebox
import psycopg2


def registre_pacient(conn, nom, cognoms,dni,adreca, telefon):
    try:

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO pacient (nom_pacient, cognoms_pacient, DNI_pacient, adreca_pacient,
            telefon_pacient)
            VALUES (%s, %s,%s,%s,%s)
        """, (nom, cognoms,dni,adreca, telefon))

        conn.commit()
        cur.close()

        messagebox.showinfo("Correcte", "Pacient registrat correctament")
    
    except Exception as e:
        messagebox.showerror("Error", str(e))


def win_registre_pacient(conn):
    root = tk.Tk()
    root.title("Alta de Pacient")
    root.geometry("350x300")

    # Labels y entradas
    tk.Label(root, text="Nom").pack()
    entry_nom = tk.Entry(root)
    entry_nom.pack()

    tk.Label(root, text="Cognoms").pack()
    entry_cognoms = tk.Entry(root)
    entry_cognoms.pack()

    tk.Label(root, text="DNI").pack()
    entry_dni = tk.Entry(root)
    entry_dni.pack()

    tk.Label(root, text="Adreça").pack()
    entry_adreca = tk.Entry(root)
    entry_adreca.pack()

    tk.Label(root, text="Telèfon").pack()
    entry_telefon = tk.Entry(root)
    entry_telefon.pack()

    # Botón guardar

    def guardar(conn):
            nom = entry_nom.get()
            cognoms = entry_cognoms.get()
            dni = entry_dni.get()
            adreca = entry_adreca.get()
            telefon = entry_telefon.get()
            if not validar_dni_nie(dni):
                messagebox.showerror("Error", "DNI o NIE no vàlid")
                return
            
            registre_pacient(conn,nom, cognoms, dni, adreca, telefon)
            root.destroy()
    tk.Button(root, text="Guardar",command=guardar).pack(pady=10)
  # Ejecutar pantalla


    root.mainloop()





def validar_dni_nie(documento):
    documento = documento.strip().upper()

    if len(documento) != 9:
        return False

    letras = "TRWAGMYFPDXBNJZSQVHLCKE"

    # DNI (8 números + letra)
    if documento[:8].isdigit():
        numero = int(documento[:8])
        letra = documento[8]
        return letras[numero % 23] == letra

    # NIE (X/Y/Z + números + letra)
    if documento[0] in "XYZ" and documento[1:8].isdigit():
        prefijo = documento[0]
        numero = documento[1:8]
        letra = documento[8]

        # Sustituir letra inicial
        if prefijo == "X":
            numero = "0" + numero
        elif prefijo == "Y":
            numero = "1" + numero
        elif prefijo == "Z":
            numero = "2" + numero

        return letras[int(numero) % 23] == letra

    return False