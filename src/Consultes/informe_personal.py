import tkinter as tk
from tkinter import ttk, messagebox


# Funció genèrica per mostrar dades
def mostrar_dades(conn, query, titol):

    try:
        cur = conn.cursor()

        win = tk.Toplevel()
        win.title(titol)
        win.geometry("800x400")

        tree = ttk.Treeview(win)
        tree.pack(fill="both", expand=True)

        cur.execute(query)
        rows = cur.fetchall()

        # Columnes automàtiques
        col_names = [desc[0] for desc in cur.description]
        tree["columns"] = col_names
        tree.column("#0", width=0, stretch=tk.NO)

        for col in col_names:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for row in rows:
            tree.insert("", "end", values=row)

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))



# Consultes SQL

def veure_metges(conn):
    query = """
        SELECT 
            'METGE' AS tipus,
            p.nom,
            p.cognoms,
            p.dni,
            m.especialitat_metge
        FROM personal p
        JOIN metge m ON p.id_personal = m.id_personal;
    """
    mostrar_dades(conn,query, "Llista de Metges")


def veure_infermers(conn):
    query = """
        SELECT 
            'INFERMER' AS tipus,
            p.nom,
            p.cognoms,
            p.dni,
            i.especialitat_infermeria
        FROM personal p
        JOIN infermeria i ON p.id_personal = i.id_personal;
    """
    mostrar_dades(conn,query, "Llista d'Infermers")


def veure_varis(conn):
    query = """
        SELECT 
            'VARI' AS tipus,
            p.nom,
            p.cognoms,
            p.dni,
            v.tipus_tasca
        FROM personal p
        JOIN vari v ON p.id_personal = v.id_personal;
    """
    mostrar_dades(conn,query, "Llista de Personal Vari")


def veure_tot(conn):
    query = """
        SELECT 
            'METGE' AS tipus,
            p.nom,
            p.cognoms,
            p.dni,
            m.especialitat_metge AS info
        FROM personal p
        JOIN metge m ON p.id_personal = m.id_personal

        UNION ALL

        SELECT 
            'INFERMER' AS tipus,
            p.nom,
            p.cognoms,
            p.dni,
            i.especialitat_infermeria AS info
        FROM personal p
        JOIN infermeria i ON p.id_personal = i.id_personal

        UNION ALL

        SELECT 
            'VARI' AS tipus,
            p.nom,
            p.cognoms,
            p.dni,
            v.tipus_tasca AS info
        FROM personal p
        JOIN vari v ON p.id_personal = v.id_personal;
    """
    mostrar_dades(conn,query, "Tot el Personal de l'Hospital")


# Menú principal Tkinter

def menu_informe_personal(conn):
    root = tk.Toplevel()   # ← NO crear otro Tk(), solo Toplevel
    root.title("Gestió de Personal - Hospital")
    root.geometry("400x300")

    tk.Label(root, text="INFORMES DE PERSONAL", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(root, text="Metges", width=25, command=lambda: veure_metges(conn)).pack(pady=5)
    tk.Button(root, text="Infermers", width=25, command=lambda: veure_metges(conn)).pack(pady=5)
    tk.Button(root, text="Personal Vari", width=25, command=lambda: veure_varis(conn)).pack(pady=5)
    tk.Button(root, text="Tot el Personal", width=25, command=lambda: veure_tot(conn)).pack(pady=20)
