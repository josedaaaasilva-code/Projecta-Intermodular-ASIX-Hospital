import tkinter as tk
from tkinter import messagebox

from login.gestio_usuaris import login
from login.gestio_usuaris import crear_usuari

from manteniment.alta_pacient import validar_dni_nie
from pantalles.menu_admin import abrir_admin
from pantalles.menu_medico import abrir_medico
from pantalles.menu_infermer import abrir_infermer
from pantalles.menu_administracio import abrir_administracio


def iniciar_login():

    finestra = tk.Tk()
    finestra.title("Hospital Blanes")
    finestra.geometry("600x400")
    finestra.resizable(True, True)
    logo = tk.PhotoImage(file="img/logo.png")

    label_logo = tk.Label(finestra, image=logo)
    label_logo.pack()


    tk.Label(finestra, text="Usuari").pack()

    entry_user = tk.Entry(finestra)
    entry_user.pack()

    tk.Label(finestra, text="Password").pack()
    entry_pass = tk.Entry(finestra, show="*")
    entry_pass.pack()

    def fer_login():

        username = entry_user.get()
        password = entry_pass.get()

        rol, conn = login(username, password)

        if rol:

            messagebox.showinfo("Correcte", "Benvingut")

            finestra.destroy()

            if rol == "admin":
                abrir_admin(conn)

            elif rol == "metge":
                abrir_medico(conn,username)

            elif rol == "infermer":
                abrir_infermer(conn,username)

            elif rol == "administratiu":
                abrir_administracio(conn)

        else:
            messagebox.showerror("Error", "Accés denegat")

    tk.Button(
        finestra,
        text="Iniciar Sessió",
        command=fer_login,
        width=20,
        bg="green",
        fg="white"
    ).pack(pady=20)
    
    tk.Button(
    finestra,
    text="Registrar-se",
    command=abrir_registro,
    width=20,
    bg="blue",
    fg="white").pack()

    finestra.mainloop()


def abrir_registro():

    win = tk.Toplevel()
    win.title("Registrar Usuari")
    win.geometry("400x300")

    tk.Label(win, text="Nou usuari", font=("Arial", 16)).pack(pady=10)

    tk.Label(win, text="Username").pack()
    entry_user = tk.Entry(win)
    entry_user.pack()

    tk.Label(win, text="Password").pack()
    entry_pass = tk.Entry(win, show="*")
    entry_pass.pack()
    
    tk.Label(win, text="DNI").pack()
    entry_dni = tk.Entry(win,)
    entry_dni.pack()
    
    
    tk.Label(win, text="Rol").pack()

    # selector de rol
    rol_var = tk.StringVar()
    rol_var.set("metge")

    tk.OptionMenu(win, rol_var, "admin", "metge", "infermer", "administratiu").pack()

    def registrar():

        username = entry_user.get()
        password = entry_pass.get()
        dni = entry_dni.get()
        rol = rol_var.get()
        
        #convertir rol → id_rol
        mapa_roles = {
            "admin": 1,
            "metge": 2,
            "infermer": 3,
            "administratiu": 4
        }

        id_rol = mapa_roles.get(rol)

        try:
            crear_usuari(username, password,dni, id_rol)
            messagebox.showinfo("Correcte", "Usuari creat")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No s'ha pogut crear: {e}")

    tk.Button(win, text="Registrar", command=registrar, bg="blue", fg="white").pack(pady=20)
