import tkinter as tk
from tkinter import messagebox
from exportacions.exportar_json import exportar_visites_json
from exportacions.exportar_xml import exportar_visites_xml


def menu_exportacions():
    finestra = tk.Toplevel()
    finestra.title("Exportacions")

    # Etiquetes i entrades
    tk.Label(finestra, text="Data inici (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
    entry_inici = tk.Entry(finestra)
    entry_inici.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(finestra, text="Data fi (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
    entry_fi = tk.Entry(finestra)
    entry_fi.grid(row=1, column=1, padx=5, pady=5)

    # Funcions bàsiques
    def exportar_json():
        inici = entry_inici.get()
        fi = entry_fi.get()
        try:
            exportar_visites_json(inici, fi)
            messagebox.showinfo("OK", "Exportació JSON completada")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def exportar_xml():
        inici = entry_inici.get()
        fi = entry_fi.get()
        try:
            exportar_visites_xml(inici, fi)
            messagebox.showinfo("OK", "Exportació XML completada")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Botons
    tk.Button(finestra, text="Exportar JSON", command=exportar_json).grid(row=2, column=0, padx=5, pady=10)
    tk.Button(finestra, text="Exportar XML", command=exportar_xml).grid(row=2, column=1, padx=5, pady=10)
    tk.Button(finestra, text="Tancar", command=finestra.destroy).grid(row=3, column=0, columnspan=2, pady=10)