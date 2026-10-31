#imports
import tkinter as tk
from tkinter import ttk, messagebox




def mostrar_malalties(conn, tree):

    try:
        cur = conn.cursor()

        consulta = """
        SELECT
            diagnostic AS malaltia,
            COUNT(*) AS total
        FROM visita
        WHERE diagnostic IS NOT NULL AND diagnostic <> ''
        GROUP BY diagnostic
        ORDER BY total DESC;
        """

        cur.execute(consulta)
        resultats = cur.fetchall()

        #netejar taula abans d'omplir-la
        for fila in tree.get_children():
            tree.delete(fila)

        #afegir files noves
        for malaltia, total in resultats:
            tree.insert("", "end", values=(malaltia, total))

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


    #finestra principal
def mostrar_malalties_window(conn):
    win = tk.Tk()
    win.title("Malalties més comunes")
    win.geometry("450x350")

    tk.Label(win, text="Malalties més comunes registrades", font=("Arial", 14, "bold")).pack(pady=10)

    #botó per carregar dades
    tk.Button(
        win,
        text="Carregar dades",
        command=lambda: mostrar_malalties(conn, tree)
    ).pack(pady=10)

    # taula Treeview
    cols = ("Malaltia", "Total")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=10)

    tree.heading("Malaltia", text="Malaltia")
    tree.heading("Total", text="Total")

    tree.column("Malaltia", width=250)
    tree.column("Total", width=80, anchor="center")

    tree.pack(pady=10)

    win.mainloop()