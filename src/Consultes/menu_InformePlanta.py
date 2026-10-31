#imports
import tkinter as tk
from tkinter import ttk, messagebox

from login.permisos import conn

#Obtenir la planta seleccionada
def mostrar_dades_planta(conn, combo_plantes, frame_resultat):

    planta = combo_plantes.get()#llegeix la planta seleccionada

    try:
        cur = conn.cursor()#obre cursor

        #consulta sql
        #agafa la planta seleccionada, fa left join amb habitació, quirofan i infermeria.
        #compta quants elements hi ha a cada taula per aqueslla planta.
        #el distinct es simplement per evitar duplicats.
        consulta = """
        SELECT
            COUNT(DISTINCT h.id_habitacio) AS habitacions,
            COUNT(DISTINCT q.id_quirofan) AS quirofans,
            COUNT(DISTINCT i.id_personal) AS infermeria
        FROM planta p
        LEFT JOIN habitacio h
            ON p.num_planta = h.num_planta
        LEFT JOIN quirofan q
            ON p.num_planta = q.num_planta
        LEFT JOIN infermeria i
            ON p.num_planta = i.id_planta
        WHERE p.num_planta = %s;
        """
    
        #executar la consulta
        cur.execute(consulta, (planta,))
        #resultat en format tupla
        resultat = cur.fetchone()

        #esborrem contingut antic
        for widget in frame_resultat.winfo_children():
            widget.destroy()

        #primera columna: noms
        tk.Label(frame_resultat, text="Planta:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Label(frame_resultat, text="Habitacions:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Label(frame_resultat, text="Quiròfans:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Label(frame_resultat, text="Infermeria:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w", padx=5, pady=5)

        #segona columna: valors
        tk.Label(frame_resultat, text=planta, font=("Arial", 12)).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        tk.Label(frame_resultat, text=resultat[0], font=("Arial", 12)).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        tk.Label(frame_resultat, text=resultat[1], font=("Arial", 12)).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(frame_resultat, text=resultat[2], font=("Arial", 12)).grid(row=3, column=1, sticky="w", padx=5, pady=5)

        #tancar connexió
        cur.close()

    #gestió d'errors en el cas de que passi alguna cosa (connexió, SQL...).
    except Exception as e:
        messagebox.showerror("Error", str(e))

def menu_planta(conn):
   #tkinter
    #pantalla
    #tkinter
    #pantalla
    win = tk.Tk()
    win.title("Informe plantes")
    win.geometry("400x300")

    #text inicial
    tk.Label(win, text="Selecció de la planta que vols veure").pack(pady=10)

    #comobobox de plantes
    combo_plantes = ttk.Combobox(
        win,
        values=[1,2,3,4],
        state="readonly"
    )

    combo_plantes.pack(pady=10)
    combo_plantes.current(0)

    #botó per accedir
    tk.Button(
        win,
        text="Accedir",
        command=lambda:mostrar_dades_planta(conn,combo_plantes,frame_resultat)
    ).pack(pady=10)

    #marc on es mostrarà la quadrícula
    frame_resultat = tk.Frame(win)
    frame_resultat.pack(pady=20)

    win.mainloop()