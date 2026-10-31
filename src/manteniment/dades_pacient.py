import tkinter as tk
from tkinter import ttk, messagebox
from login.permisos import conn




# CONSULTA VISITES + MEDICAMENTS
def veure_visites_medicaments(conn,id_pacient, tree):
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                v.id_visita,
                v.data,
                v.hora,
                v.diagnostic,
                m.nom_medicament,
                mr.dosi,
                mr.frequencia
            FROM visita v
            LEFT JOIN medicament_receptat mr ON v.id_visita = mr.id_visita
            LEFT JOIN medicament m ON mr.id_medicament = m.id_medicament
            WHERE v.id_pacient = %s and v.data <= CURRENT_DATE
            ORDER BY v.data, v.hora;
        """, (id_pacient,))

        rows = cur.fetchall()

        # Limpiar tabla
        for item in tree.get_children():
            tree.delete(item)

        if not rows:
            messagebox.showinfo("Sense visites", "Aquest pacient no té visites registrades.")
            return

        # Insertar filas
        for row in rows:
            id_visita, data, hora, diag, nom_med, dosi, freq = row
            tree.insert("", "end", values=(
                id_visita,
                data,
                hora,
                diag,
                nom_med if nom_med else "—",
                dosi if dosi else "—",
                freq if freq else "—"
            ))

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# CONSULTA INGRESOS 

def veure_ingressos_window(conn,id_pacient):
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                r.data_ingres_prevista,
                r.data_sortida_prevista,
                h.num_habitacio
                
            FROM reserva_habitacio r
            LEFT join habitacio h on h.num_habitacio= r.id_habitacio    
            WHERE r.id_pacient = %s and data_ingres_prevista <= CURRENT_DATE
            ORDER BY r.data_ingres_prevista;
        """, (id_pacient,))

        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("Ingressos", "Aquest pacient NO ha estat ingressat.")
            return

        # Crear finestra
        win = tk.Toplevel()
        win.title("Ingressos del pacient")
        win.geometry("600x400")

        tree = ttk.Treeview(win)
        tree["columns"] = ("Data Ingrés", "Data Sortida", "Habitació")

        tree.column("#0", width=0, stretch=tk.NO)
        for col in tree["columns"]:
            tree.column(col, width=150)

        for col in tree["columns"]:
            tree.heading(col, text=col)

        tree.pack(fill="both", expand=True, pady=10)

        # Insertar datos
        for row in rows:
            data_in, data_out, habit = row
            tree.insert("", "end", values=(data_in, data_out, habit))

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))
    tk.Button(win, text="Tancar", command=win.destroy).pack(pady=10)




#CONSULTA OPERACIONS 

def veure_operacions_window(conn,id_pacient):
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                o.data_operacio,
                o.hora_operacio,
                o.id_quirofan,
                per.nom,
                per.cognoms
            FROM operacio o
            JOIN personal per ON o.id_metge = per.id_personal
            WHERE o.id_pacient = %s and o.data_operacio<=CURRENT_DATE
            ORDER BY o.data_operacio, o.hora_operacio;
        """, (id_pacient,))

        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("Operacions", "Aquest pacient NO té operacions registrades.")
            return

        # Crear finestra
        win = tk.Toplevel()
        win.title("Operacions del pacient")
        win.geometry("700x400")

        tree = ttk.Treeview(win)
        tree["columns"] = ("Data", "Hora", "Quiròfan", "Metge", "Cognoms")

        tree.column("#0", width=0, stretch=tk.NO)
        for col in tree["columns"]:
            tree.column(col, width=120)

        for col in tree["columns"]:
            tree.heading(col, text=col)

        tree.pack(fill="both", expand=True, pady=10)

        # Insertar datos
        for row in rows:
            data, hora, quir, nom, cognoms = row
            tree.insert("", "end", values=(data, hora, quir, nom, cognoms))

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))
    tk.Button(win, text="Tancar", command=win.destroy).pack(pady=10)



#FINESTRA PRINCIPAL 

def menu_pacient(conn):

    win = tk.Toplevel()
    win.title("Informació del pacient")
    win.geometry("900x500")

    tk.Label(win, text="ID Pacient:", font=("Arial", 12)).pack(pady=5)
    entry_id = tk.Entry(win)
    entry_id.pack(pady=5)

    # Tabla visitas + medicaments
    tree = ttk.Treeview(win)
    tree["columns"] = ("ID Visita", "Data", "Hora", "Diagnòstic", "Medicament", "Dosi", "Freqüència")

    tree.column("#0", width=0, stretch=tk.NO)
    for col in tree["columns"]:
        tree.column(col, width=120)

    for col in tree["columns"]:
        tree.heading(col, text=col)

    tree.pack(pady=20, fill="both", expand=True)

    # Botones
    frame_btn = tk.Frame(win)
    frame_btn.pack(pady=10)

    tk.Button(
        frame_btn,
        text="Veure visites i medicaments",
        command=lambda: veure_visites_medicaments(conn,entry_id.get(), tree)
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        frame_btn,
        text="Ingressos",
        command=lambda: veure_ingressos_window(conn,entry_id.get())
    ).grid(row=0, column=1, padx=10)

    tk.Button(
        frame_btn,
        text="Operacions",
        command=lambda: veure_operacions_window(conn,entry_id.get())
    ).grid(row=0, column=2, padx=10)

    tk.Button(win, text="Tancar", command=win.destroy).pack(pady=10)
    win.mainloop()



