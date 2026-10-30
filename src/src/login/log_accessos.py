import psycopg2


def registrar_log(username, resultat):
    """
    Guarda login correcto o incorrecto
    """

    conn = psycopg2.connect(
        host="192.168.56.103",
        database="hospital",
        user="postgres",
        password="1234"
    )

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO logs_accessos (username, resultat)
        VALUES (%s, %s)
    """, (username, resultat))

    conn.commit()
    cur.close()
    conn.close()

#guarda:
#admin: LOGIN CORRECT
#juan: PASSWORD INCORRECT