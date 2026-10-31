import tkinter as tk
from tkinter import ttk, messagebox

def veure_aparells_quirofan(conn,id_quirofan):

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                ta.nom_tipus,
                aq.quantitat
            FROM aparell_en_quirofan aq
            JOIN aparell_medic am ON aq.id_aparell = am.id_aparell
            JOIN tipus_aparell ta ON am.id_tipus = ta.id_tipus
            WHERE aq.id_quirofan = %s
            ORDER BY ta.nom_tipus;
        """, (id_quirofan,))

        rows = cur.fetchall()

        if len(rows) == 0:
            messagebox.showinfo("Aparells", "Aquest quiròfan NO té aparells assignats.")
            return

        win = tk.Toplevel()
        win.title(f"Aparells del quiròfan {id_quirofan}")
        win.geometry("500x300")

        tree = ttk.Treeview(win)
        tree["columns"] = ("aparell", "quantitat")

        tree.column("#0", width=0)
        tree.column("aparell", width=250)
        tree.column("quantitat", width=100)

        tree.heading("aparell", text="Aparell")
        tree.heading("quantitat", text="Quantitat")

        tree.pack(fill="both", expand=True)

        for fila in rows:
            tree.insert("", "end", values=fila)

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def menu_quirofan(conn):
    win = tk.Toplevel()
    win.title("Consultar aparells del quiròfan")
    win.geometry("350x200")

    tk.Label(win, text="ID Quiròfan:", font=("Arial", 12)).pack(pady=10)

    entry_id = tk.Entry(win)
    entry_id.pack(pady=5)

    tk.Button(
        win,
        text="Executar",
        command=lambda: veure_aparells_quirofan(conn, entry_id.get())
    ).pack(pady=15)
