from tkinter import messagebox, ttk
import tkinter as tk


def informe_visites_per_dia(conn):
    try:
        cur = conn.cursor()

        query = """
            SELECT 
                data AS dia,
                COUNT(*) AS nombre_visites
            FROM visita
            GROUP BY data
            ORDER BY data;
        """

        cur.execute(query)
        rows = cur.fetchall()

        win = tk.Toplevel()
        win.title("Informe de visites per dia")
        win.geometry("500x400")

        tree = ttk.Treeview(win)
        tree["columns"] = ("Dia", "Nombre de visites")

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Dia", width=150)
        tree.column("Nombre de visites", width=150)

        tree.heading("Dia", text="Dia")
        tree.heading("Nombre de visites", text="Nombre de visites")

        tree.pack(fill="both", expand=True)

        for row in rows:
            tree.insert("", "end", values=row)

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))
