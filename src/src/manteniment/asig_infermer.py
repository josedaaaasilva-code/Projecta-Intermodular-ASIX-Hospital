import tkinter as tk
from tkinter import ttk, messagebox


import tkinter as tk
from tkinter import ttk, messagebox

def win_veure_assig(conn, username):

    win = tk.Toplevel()
    win.title("Assignació Infermeria")
    win.geometry("600x400")

    tk.Label(win, text=f"Assignació de: {username}", font=("Arial", 14)).pack(pady=10)

    # Taula simplificada (només una columna)
    tree = ttk.Treeview(win)
    tree["columns"] = ("Assignacio",)

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Assignacio", anchor=tk.W, width=500)

    tree.heading("Assignacio", text="Assignació")

    tree.pack(pady=20, fill="both", expand=True)


    def carregar_assignacio():

        try:
            cur = conn.cursor()

            # Obtenir metge assignat o planta
            cur.execute("""
                SELECT 
                    m.nom AS nom_metge,
                    m.cognoms AS cognoms_metge,
                    i.id_planta
                FROM infermeria i
                JOIN personal p ON p.id_personal = i.id_personal
                JOIN usuaris u ON u.dni = p.dni
                LEFT JOIN personal m ON m.id_personal = i.id_metge
                WHERE u.username = %s
            """, (username,))

            row = cur.fetchone()

            if not row:
                messagebox.showinfo("Sense dades", "No s'ha trobat cap assignació")
                return

            nom_metge, cognoms_metge, id_planta = row

            # Determinar què mostrar
            if nom_metge is not None:
                assignacio = f"Metge assignat: {nom_metge} {cognoms_metge}"
            else:
                assignacio = f"Planta assignada: {id_planta}"

            # Netejar taula
            for item in tree.get_children():
                tree.delete(item)

            # Inserir només la informació necessària
            tree.insert("", "end", values=(assignacio,))

            cur.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Botó carregar
    tk.Button(win, text="Carregar assignació",
              command=carregar_assignacio).pack(pady=10)

    # Botó tancar
    tk.Button(win, text="Tancar", command=win.destroy).pack(pady=10)


def veure_companys_infermer(conn, username):
    # Crear conexión con rol infermer
    if conn is None:
        messagebox.showerror("Error", "No s'ha pogut connectar a la base de dades")
        return
    
    cur = conn.cursor()

    # Obtenir id_metge associat a l'infermer actual
    cur.execute("""
        SELECT i.id_metge
        FROM infermeria i
        JOIN personal p ON p.id_personal = i.id_personal
        JOIN usuaris u ON u.dni = p.dni
        WHERE u.username = %s
    """, (username,))

    result = cur.fetchone()
    if not result or result[0] is None:
        messagebox.showinfo("Informació", "No tens cap metge assignat.")
        return
    
    id_metge_assignat = result[0]
    
    #Obtenció de companys infermers que depenen del mateix metge, excepte el propi infermer
    cur.execute("""
        SELECT p.nom, p.cognoms
        FROM infermeria i
        JOIN personal p ON p.id_personal = i.id_personal
        WHERE i.id_metge = %s
        AND p.dni != (SELECT dni FROM usuaris WHERE username = %s)
    """, (id_metge_assignat, username))

    companys = cur.fetchall()

    # Crear finestra Tkinter
    win = tk.Toplevel()
    win.title("Companys d'infermeria assignats al mateix metge")
    win.geometry("500x300")

    tree = ttk.Treeview(win, columns=("Nom", "Cognoms"), show="headings")
    tree.heading("Nom", text="Nom")
    tree.heading("Cognoms", text="Cognoms")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for nom, cognoms in companys:
        tree.insert("", "end", values=(nom, cognoms))

    if not companys:
        messagebox.showinfo("Informació", "No tens companys assignats al mateix metge.")

    tk.Button(win, text="Tancar", command=win.destroy).pack(pady=10)
    cur.close()