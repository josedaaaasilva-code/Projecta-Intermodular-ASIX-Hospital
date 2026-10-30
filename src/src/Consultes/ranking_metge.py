from tkinter import messagebox, ttk
import tkinter as tk




def ranking_metges(conn):
    try:
        cur = conn.cursor()

        query = """
            SELECT 
                per.nom,
                per.cognoms,
                per.dni,
                COUNT(v.id_pacient) AS pacients_atessos
            FROM visita v
            JOIN personal per ON v.id_metge = per.id_personal
            GROUP BY per.nom, per.cognoms, per.dni
            ORDER BY pacients_atessos DESC;
        """

        cur.execute(query)
        rows = cur.fetchall()

        win = tk.Toplevel()
        win.title("Rànquing de metges que atenen més pacients")
        win.geometry("600x400")

        tree = ttk.Treeview(win)
        tree["columns"] = ("Nom", "Cognoms", "DNI", "Pacients atesos")

        tree.column("#0", width=0, stretch=tk.NO)
        for col in tree["columns"]:
            tree.column(col, width=150)
            tree.heading(col, text=col)

        tree.pack(fill="both", expand=True)

        for row in rows:
            tree.insert("", "end", values=row)

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))
