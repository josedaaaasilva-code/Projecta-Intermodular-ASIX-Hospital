import tkinter as tk
from login.gestio_usuaris import tornar_login
from manteniment.asig_infermer import veure_companys_infermer, win_veure_assig

def win_veure_assistencia(conn, username):
    raise NotImplementedError

def abrir_infermer(conn,username):

    win = tk.Tk()
    win.title("Infermer")
    win.geometry("400x350")
    cur = conn.cursor()

    # proba real de permisos
   
    
    tk.Label(win, text="MENU INFERMER", font=("Arial", 18)).pack(pady=20)

    tk.Button(win, text="asignacions",command=lambda:win_veure_assig(conn,username), width=25).pack(pady=5)
    tk.Button(win, text="veure companys",command=lambda: veure_companys_infermer(conn,username), width=25).pack(pady=5)

    tk.Button(win, text="Sortir", command=win.destroy).pack(pady=20)
    tk.Button(win, text="Tornar al login", command=lambda: tornar_login(win)).pack(pady=20)

    win.mainloop()