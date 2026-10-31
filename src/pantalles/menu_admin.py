import tkinter as tk
from Consultes.menu_InformePlanta import mostrar_dades_planta
from dummy.esborrar_dummy import borrar_todo
from dummy.generar_dummy import generar_todo
from exportacions.menu_exportacions import menu_exportacions
from login.gestio_usuaris import tornar_login
from manteniment.alta_personal import finestra_alta_personal


def abrir_admin(conn):

    win = tk.Tk()
    win.title("Panel Admin")
    win.geometry("400x350")

    cur = conn.cursor()

    # Títol
    tk.Label(win, text="MENU ADMIN", font=("Arial", 18)).pack(pady=20)

    # Botons del menú
   
    tk.Button(win, text="exportacions",command=menu_exportacions, width=25).pack(pady=5)

    tk.Button(win, text="Generar Dummy Data", command=generar_todo).pack()
    tk.Button(win, text="Eliminar Dummy Data", command=borrar_todo).pack()

    tk.Button(win, text="Alta de personal",
              command=lambda: finestra_alta_personal(conn)).pack(pady=5)

    tk.Button(win, text="Sortir", command=win.destroy).pack(pady=20)

    tk.Button(
        win,
        text="Tornar al login",
        command=lambda: tornar_login(win)
    ).pack(pady=10)

    win.mainloop()
