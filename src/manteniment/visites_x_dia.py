import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def veure_visites_per_dia(conn,data, tree):

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                v.hora,
               nom_pacient,
                cognoms_pacient,
                per.nom AS nom_metge,
                per.cognoms AS cognoms_metge
            FROM visita v
            JOIN pacient p ON v.id_pacient = p.id_pacient
            JOIN metge m ON v.id_metge = m.id_personal
            JOIN personal per ON m.id_personal = per.id_personal
            WHERE v.data = %s
            ORDER BY v.hora;
        """, (data,))

        rows = cur.fetchall()

        # Netejar taula
        for item in tree.get_children():
            tree.delete(item)

        # Inserir dades
        for row in rows:
            hora, nom_pac, cogn_pac, nom_met, cogn_met = row
            tree.insert("", "end", values=(
                hora,
                f"{nom_pac} {cogn_pac}",
                f"{nom_met} {cogn_met}"
            ))

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def finestra_visites(conn):

    win = tk.Toplevel()
    win.title("Visites per dia")
    win.geometry("600x400")

    tk.Label(win, text="Introdueix la data (YYYY-MM-DD)").pack()

    entry_data = tk.Entry(win)
    entry_data.pack(pady=5)

    # Crear Treeview
    tree = ttk.Treeview(win)
    tree["columns"] = ("Hora", "Pacient", "Metge")

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Hora", width=80)
    tree.column("Pacient", width=200)
    tree.column("Metge", width=200)

    tree.heading("Hora", text="Hora")
    tree.heading("Pacient", text="Pacient")
    tree.heading("Metge", text="Metge")

    tree.pack(pady=20, fill="both", expand=True)

    # Botó per buscar visites
    tk.Button(
        win,
        text="Cercar visites",
        command=lambda: veure_visites_per_dia(conn,entry_data.get(), tree)
    ).pack(pady=10)

    tk.Button(win, text="Tancar", command=win.destroy).pack(pady=10)