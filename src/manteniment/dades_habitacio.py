import tkinter as tk
from tkinter import messagebox, ttk


def veure_reserves_habitacio_window(conn,id_habitacio):
 
    try:
        cur = conn.cursor()

        # Consulta simple
        cur.execute("""
            SELECT 
                r.data_ingres_prevista,
                r.data_sortida_prevista,
                p.nom_pacient
            FROM reserva_habitacio r
            JOIN pacient p ON r.id_pacient = p.id_pacient
            WHERE r.id_habitacio = %s
            ORDER BY r.data_ingres_prevista;
        """, (id_habitacio,))

        rows = cur.fetchall()

        # Si no hay reservas → mensaje
        if len(rows) == 0:
            messagebox.showinfo("Reserves", "Aquesta habitació NO té reserves previstes.")
            return

        # Ventana simple
        win = tk.Toplevel()
        win.title("Reserves habitació " + str(id_habitacio))
        win.geometry("600x300")

        # Tabla simple
        tree = ttk.Treeview(win)
        tree["columns"] = ("ingres", "sortida", "pacient")

        tree.column("#0", width=0)
        tree.column("ingres", width=150)
        tree.column("sortida", width=150)
        tree.column("pacient", width=200)

        tree.heading("ingres", text="Data ingrés")
        tree.heading("sortida", text="Data sortida")
        tree.heading("pacient", text="Pacient")

        tree.pack(fill="both", expand=True)

        # Insertar filas
        for fila in rows:
            tree.insert("", "end", values=fila)

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))
