
import psycopg2
def get_conn():
    return psycopg2.connect(
        host="192.168.56.103",
        database="hospital",
        user="postgres",
        password="1234"
    )
        

def obtenir_visites_entre_dates(data_inici, data_fi):
    
    conn=get_conn()
    cursor = conn.cursor()

    query = """ SELECT
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

    cursor.execute(query, (data_inici, data_fi))
    resultats = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultats