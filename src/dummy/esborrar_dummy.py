# dummy/esborrar_dummy.py
import tkinter as tk
from tkinter import messagebox

from dummy.generar_dummy import conn


def borrar_todo():
    """Elimina TOTES les dades de la base de dades"""
    
    root = tk.Tk()
    root.withdraw()
    
    result = messagebox.askyesno(
        "ALERTA!",
        "⚠️ Això ELIMINARÀ TOTES les dades de la base de dades.\n"
        "Aquesta acció NO es pot desfer.\n\n"
        "Estàs completament SEGUR?"
    )
    
    if not result:
        root.destroy()
        return
    
    root.destroy()

    
    try:
        cur = conn.cursor()
        
        # Ordre correcte: primer taules amb FK, després les principals
        taules = [
            'assistencia_operacio',
            'medicament_receptat',
            'reserva_habitacio',
            'operacio',
            'visita',
            'horari_metge',
            'aparell_en_quirofan',
            'infermeria',
            'vari',
            'metge',
            'usuaris',
            'pacient',
            'personal',
            'aparell_medic',
            'tipus_aparell',
            'quirofan',
            'habitacio',
            'planta'
        ]
        
        for taula in taules:
            try:
                cur.execute(f"DELETE FROM {taula}")
                print(f"{taula}: {cur.rowcount} registres eliminats")
            except Exception as e:
                print(f"{taula}: {e}")
        
        conn.commit()
        messagebox.showinfo("Èxit", "Totes les dades han estat eliminades correctament!")
        print("Neteja completada!")
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Error", f"Error eliminant dades:\n{str(e)}")
        print(f"ERROR: {e}")
