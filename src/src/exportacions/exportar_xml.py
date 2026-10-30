import xml.etree.ElementTree as ET
from datetime import datetime
import os
from exportacions.utils_exportacio import get_conn



def exportar_visites_xml(inici, fi):

    try:
        # Crear conexión y cursor
        conn=get_conn()
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

        # Crear estructura XML
        arrel = ET.Element("visites")

        for fila in resultats:
            visita = ET.SubElement(arrel, "visita")

            ET.SubElement(visita, "id_visita").text = str(fila[0])
            ET.SubElement(visita, "data").text = str(fila[1])
            ET.SubElement(visita, "area").text = str(fila[2])
            ET.SubElement(visita, "hora").text = str(fila[3])

            pacient = ET.SubElement(visita, "pacient")
            ET.SubElement(pacient, "dni").text = fila[4]
            ET.SubElement(pacient, "nom").text = fila[5]
            ET.SubElement(pacient, "cognoms").text = fila[6]

            metge = ET.SubElement(visita, "metge")
            ET.SubElement(metge, "nom").text = fila[7]
            ET.SubElement(metge, "cognoms").text = fila[8]

            ET.SubElement(visita, "diagnostic").text = fila[9]


        # Crear carpeta si no existe
        os.makedirs("exportacions", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_fitxer = f"exportacions/historial_xml/visites_{timestamp}.xml"

        arbre = ET.ElementTree(arrel)
        arbre.write(nom_fitxer, encoding="utf-8", xml_declaration=True)

        print(f"XML exportat correctament: {nom_fitxer}")

    except Exception as e:
        print(f"Error exportant XML: {e}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()