import tkinter as tk
from Consultes.malalties import mostrar_malalties, mostrar_malalties_window
from login.gestio_usuaris import tornar_login
from manteniment.dades_habitacio import veure_reserves_habitacio_window
from manteniment.dades_pacient import menu_pacient
from manteniment.operacio_visita_metge import veure_hores_metge, veure_operacions_metge, veure_visites_metge

def abrir_medico(conn,username):

    win = tk.Tk()
    win.title("Panel Metge")
    win.geometry("400x350")

    cur = conn.cursor()

    # proba real de permisos

    tk.Label(win, text="MENU METGE", font=("Arial", 18)).pack(pady=20)
    tk.Button(win, text="Dades malalties",command=lambda: mostrar_malalties_window(conn),width=25).pack(pady=5)

    tk.Button(win, text="Dades Habitació",command=lambda: veure_reserves_habitacio_window(conn, entry_habitacio.get()),width=25).pack(pady=5)
    tk.Label(win, text="ID Habitació:", font=("Arial", 12)).pack(pady=5)
    entry_habitacio = tk.Entry(win)
    entry_habitacio.pack(pady=20)
    
    tk.Button(win, text="Visites", command=lambda: veure_visites_metge(conn,username),padx=20).pack(pady=5)
    tk.Button(win, text="Operacions", command=lambda: veure_operacions_metge(conn,username),padx=5).pack(pady=5)
    tk.Button(win, text="Hores disponibles", command=lambda: veure_hores_metge(conn,username)).pack(pady=5)

    tk.Button(win, text="Obrir menú pacient", command=lambda: menu_pacient(conn)).pack(pady=5)

    tk.Button(win, text="Sortir", command=win.destroy).pack(pady=20)
    tk.Button(win, text="Tornar al login", command=lambda: tornar_login(win)).pack(pady=20)

    win.mainloop()