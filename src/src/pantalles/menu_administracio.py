import tkinter as tk
from Consultes.informe_nombre_visites import informe_visites_per_dia
from Consultes.informe_personal import menu_informe_personal
from Consultes.menu_InformePlanta import menu_planta
from Consultes.ranking_metge import ranking_metges
from login.gestio_usuaris import tornar_login
from manteniment.alta_pacient import win_registre_pacient
from manteniment.aparell_quirofan import menu_quirofan, veure_aparells_quirofan
from manteniment.visites_x_dia import finestra_visites

def abrir_administracio(conn):

    win = tk.Tk()
    win.title("Administració")
    win.geometry("400x350")
    cur = conn.cursor()

    # proba real de permisos)
    tk.Label(win, text="MENU ADMINISTRACIÓ", font=("Arial", 18)).pack(pady=20)

    tk.Button(win, text="Alta pacients", command=lambda: win_registre_pacient(conn), width=25).pack(pady=5)
    tk.Button(win, text="Visites",command=lambda: finestra_visites(conn), width=25).pack(pady=5)

    tk.Button(win, text="Informe visites per dia", command=lambda: informe_visites_per_dia(conn)).pack(pady=5)
    tk.Button(win, text="Veure informació de la planta", command=lambda: menu_planta(conn), width=25).pack(pady=5)


    tk.Button(win, text="Aparells quiròfan", command=lambda: menu_quirofan(conn)).pack(pady=5)
    tk.Button(win, text="Personal", command=lambda: menu_informe_personal(conn)).pack(pady=5)
    tk.Button(win, text="ranking", command=lambda: ranking_metges(conn)).pack(pady=5)


    tk.Button(win, text="Sortir", command=win.destroy).pack(pady=20)
    tk.Button(win, text="Tornar al login", command=lambda: tornar_login(win)).pack(pady=20)

    win.mainloop()