import tkinter as tk
from tkinter import ttk, messagebox

def veure_visites_metge(conn, username):
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                v.data,
                v.hora,
                pa.nom_pacient
            FROM visita v
            JOIN pacient pa ON v.id_pacient = pa.id_pacient
            WHERE v.id_metge = (
                SELECT id_personal 
                FROM personal pe
                JOIN usuaris us ON pe.dni = us.dni
                WHERE us.username = %s
            )
            ORDER BY v.data, v.hora
                    ;
        """, (username,))

        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("Visites", "Aquest metge NO té visites programades.")
            return

        win = tk.Toplevel()
        win.title("Visites del metge")
        win.geometry("600x300")

        tree = ttk.Treeview(win, columns=("data", "hora", "pacient"), show="headings")
        tree.heading("data", text="Data")
        tree.heading("hora", text="Hora")
        tree.heading("pacient", text="Pacient")

        tree.column("data", width=150)
        tree.column("hora", width=150)
        tree.column("pacient", width=250)

        tree.pack(fill="both", expand=True)

        for fila in rows:
            tree.insert("", "end", values=fila)

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- OPERACIONS ----------------
def veure_operacions_metge(conn, username):
    try:
        win = tk.Toplevel()
        win.title("Operacions del metge")
        win.geometry("900x400")

        tk.Label(win, text="Introdueix la data (YYYY-MM-DD)").pack()

        entry_data = tk.Entry(win)
        entry_data.pack(pady=5)

        tree = ttk.Treeview(win, columns=("data", "hora", "quirofan", "pacient", "infermers"), show="headings")
        tree.heading("data", text="Data")
        tree.heading("hora", text="Hora")
        tree.heading("quirofan", text="Quiròfan")
        tree.heading("pacient", text="Pacient")
        tree.heading("infermers", text="Infermers")

        tree.column("data", width=120)
        tree.column("hora", width=100)
        tree.column("quirofan", width=80)
        tree.column("pacient", width=200)
        tree.column("infermers", width=350)

        tree.pack(fill="both", expand=True)

        def buscar():
            data = entry_data.get().strip()

            if not data:
                messagebox.showwarning("Error", "Has d'introduir una data.")
                return

            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    o.data_operacio,
                    o.hora_operacio,
                    o.id_quirofan,
                    p.nom_pacient,
                    STRING_AGG(CONCAT(i.nom, ' ', i.cognoms), ', ') AS infermers
                FROM operacio o
                JOIN pacient p ON o.id_pacient = p.id_pacient
                LEFT JOIN assistencia_operacio ao ON o.id_operacio = ao.id_operacio
                LEFT JOIN personal i ON ao.id_infermeria = i.id_personal
                WHERE o.id_metge = (
                    SELECT pe.id_personal
                    FROM personal pe
                    JOIN usuaris us ON pe.dni = us.dni
                    WHERE us.username = %s
                )
                AND o.data_operacio = %s
                GROUP BY o.id_operacio, o.data_operacio, o.hora_operacio, o.id_quirofan, p.nom_pacient
                ORDER BY o.data_operacio, o.hora_operacio;
            """, (username, data))

            rows = cur.fetchall()

            tree.delete(*tree.get_children())

            if not rows:
                messagebox.showinfo("Operacions", "Aquest metge NO té operacions programades en aquesta data.")
                cur.close()
                return

            for fila in rows:
                tree.insert("", "end", values=fila)

            cur.close()

        tk.Button(win, text="Buscar", command=buscar).pack(pady=5)

    except Exception as e:
        messagebox.showerror("Error", str(e))



# ---------------- HORES DISPONIBLES ----------------
def veure_hores_metge(conn,username):
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT dia_setmana, hora_inici, hora_fi
            FROM horari_metge
            WHERE id_metge = (select id_personal 
                                    from personal pe
                                    inner join usuaris us on pe.dni=us.dni
                                        where us.username = %s );
        """, (username,))

        rows = cur.fetchall()

        if len(rows) == 0:
            messagebox.showinfo("Horari", "Aquest metge NO té hores disponibles registrades.")
            return

        win = tk.Toplevel()
        win.title("Hores disponibles")
        win.geometry("500x300")

        tree = ttk.Treeview(win)
        tree["columns"] = ("dia", "inici", "fi")

        tree.column("#0", width=0)
        tree.column("dia", width=150)
        tree.column("inici", width=150)
        tree.column("fi", width=150)

        tree.heading("dia", text="Dia")
        tree.heading("inici", text="Inici")
        tree.heading("fi", text="Fi")

        tree.pack(fill="both", expand=True)

        for fila in rows:
            tree.insert("", "end", values=fila)

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


