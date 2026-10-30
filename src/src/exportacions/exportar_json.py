import json
from datetime import datetime
import os

from exportacions.utils_exportacio import get_conn


def exportar_visites_json(inici, fi):
    conn = get_conn()
    try:
        # Crear connexió i cursor
        cursor = conn.cursor()

        query = """
      SELECT
    v.id_visita,
    v.data,
    m.especialitat_metge AS area,
    v.hora,
    p.dni_pacient,
    p.nom_pacient,
    p.cognoms_pacient,
    pe.nom AS nom_metge,
    pe.cognoms AS cognoms_metge,
    v.diagnostic
    FROM
        public.visita v
    INNER JOIN
        public.metge m ON v.id_metge = m.id_personal
    INNER JOIN
        public.pacient p ON v.id_pacient = p.id_pacient
        INNER JOIN
            public.personal pe ON m.id_personal = pe.id_personal
        where v.data between %s and %s
        ORDER BY v.data, v.hora;
        """

        cursor.execute(query, (inici, fi))
        resultats = cursor.fetchall()

        dades = {"visites": []}

        for fila in resultats:
            visita = {
                "id_visita": fila[0],
                "data": str(fila[1]),
                "area": str(fila[2]),
                "hora": str(fila[3]),
                "pacient": {
                    "dni": fila[4],
                    "nom": fila[5],
                    "cognoms": fila[6]
                },
                "metge": {
                    "nom": fila[7],
                    "cognoms": fila[8]
                },
                "diagnostic": fila[9]
            }
            dades["visites"].append(visita)


        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_fitxer = f"exportacions/historial_json/visites_{timestamp}.json"
        # Crear carpeta si no existeix
        os.makedirs("/historial_json", exist_ok=True)

        with open(nom_fitxer, "w", encoding="utf-8") as f:
            json.dump(dades, f, indent=4, ensure_ascii=False)

        print(f"JSON exportat correctament: {nom_fitxer}")

    except Exception as e:
        print(f"Error exportant JSON: {e}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()