import psycopg2

MAPEIG_ROLES = {
    "admin": ("admin_user", "admin"),
    "metge": ("metge_user", "metge"),
    "infermer": ("infermer_user", "infermer"),
    "administratiu": ("administratiu_user", "administratiu")
}
conn = None

def get_conn(user_db, pass_db):
    conn = psycopg2.connect(
        host="192.168.56.103",
        database="hospital",
        user=user_db,
        password=pass_db
    )
    conn.autocommit = True
    return conn
    


def conectar_segons_rol(rol):
    global conn
    
    if rol not in MAPEIG_ROLES:
        return None

    user_db, pass_db = MAPEIG_ROLES[rol]

    try:
        conn = get_conn(user_db, pass_db)
        return conn
    except Exception as e:
        print("ERROR CONEXION:", e)
        return None



