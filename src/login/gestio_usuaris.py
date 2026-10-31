import psycopg2
from login.permisos import conectar_segons_rol
from login.hashing import generar_hash, verificar_password
from login.log_accessos import registrar_log



#conexio bbdd


#crea usuari
def crear_usuari(username, password,dni, id_rol):

    conn = psycopg2.connect(
        host="192.168.56.103",
        database="hospital",
        user="postgres",
        password="1234"
    )

    cur = conn.cursor()

    hash_segura = generar_hash(password)

    cur.execute("""
        INSERT INTO usuaris (username, password_hash,dni,id_rol)
        VALUES (%s, %s, %s,%s)
    """, (username, hash_segura,dni,id_rol))

    conn.commit()
    cur.close()
    conn.close()

    print("Usuari creat correctament")
#crea admin.
#crear_usuari("admin","1234", 1)
#crea admin.

#login
def login(username, password):

    conn = psycopg2.connect(
        host="192.168.56.103",
        database="hospital",
        user="postgres",
        password="1234"
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT u.password_hash,
               u.intents_fallits,
               u.bloquejat,
               r.nom_rol
        FROM usuaris u
        JOIN roles r ON u.id_rol = r.id_rol
        WHERE username = %s
    """, (username,))

    resultat = cur.fetchone()

    if not resultat:
        registrar_log(username, "USUARI NO EXISTEIX")
        return None

    hash_guardado = resultat[0]
    intents = resultat[1]
    bloquejat = resultat[2]
    rol = resultat[3]

    #rol=login("admin", "1234")
    #retorna:
    #admin

    # Usuario bloqueado
    if bloquejat:
        registrar_log(username, "USUARI BLOQUEJAT")
        print("Compte bloquejat")
        return None

    # Password correcta
    if verificar_password(password, hash_guardado):

        cur.execute("""
            UPDATE usuaris
            SET intents_fallits = 0
            WHERE username = %s
        """, (username,))

        conn.commit()

        registrar_log(username, "LOGIN CORRECTE")

        cur.close()
        conn.close()

        return rol

    # Password incorrecta
    else:

        intents += 1

        if intents >= 3:
            cur.execute("""
                UPDATE usuaris
                SET intents_fallits = %s,
                    bloquejat = TRUE
                WHERE username = %s
            """, (intents, username))

            registrar_log(username, "BLOQUEJAT PER INTENTS")

        else:
            cur.execute("""
                UPDATE usuaris
                SET intents_fallits = %s
                WHERE username = %s
            """, (intents, username))

            registrar_log(username, "PASSWORD INCORRECTE")

        conn.commit()

    cur.close()
    conn.close()

    return None
#si falla 3 vegades bloqueja la compte.

#desbloquejar
def desbloquear_usuari(username):

    conn = psycopg2.connect(
        host="192.168.56.103",
        database="hospital",
        user="postgres",
        password="1234"
    )

    cur = conn.cursor()

    cur.execute("""
        UPDATE usuaris
        SET bloquejat = FALSE,
            intents_fallits = 0
        WHERE username = %s
    """, (username,))

    conn.commit()
    cur.close()
    conn.close()

    print("Usuari desbloquejat")
#desbloquear_usuari("admin")
    #crea admin.

def login(username, password):

    conn = psycopg2.connect(
        host="192.168.56.103",
        database="hospital",
        user="postgres",
        password="1234"
    )

    cur = conn.cursor()

    
    cur.execute("""
        SELECT u.password_hash,
               u.intents_fallits,
               u.bloquejat,
               r.nom_rol
        FROM usuaris u
        JOIN roles r ON u.id_rol = r.id_rol
        WHERE username = %s
    """, (username,))

    resultat = cur.fetchone()

    if not resultat:
        registrar_log(username, "USUARI NO EXISTEIX")
        return None, None

    hash_guardado = resultat[0]
    intents = resultat[1]
    bloquejat = resultat[2]
    rol = resultat[3]

    if bloquejat:
        registrar_log(username, "USUARI BLOQUEJAT")
        return None, None

    # PASSWORD CORRECTA
    if verificar_password(password, hash_guardado):

        conn_rol = conectar_segons_rol(rol)

        if not conn_rol:
            registrar_log(username, "ERROR CONEXIO ROL")
            return None, None

        cur.execute("""
            UPDATE usuaris
            SET intents_fallits = 0
            WHERE username = %s
        """, (username,))
        conn.commit()

        registrar_log(username, "LOGIN CORRECTE")

        cur.close()
        conn.close()
            
        return rol, conn_rol
    

    #  PASSWORD INCORRECTA
    else:

        intents += 1

        if intents >= 3:
            cur.execute("""
                UPDATE usuaris
                SET intents_fallits = %s,
                    bloquejat = TRUE
                WHERE username = %s
            """, (intents, username))

            registrar_log(username, "BLOQUEJAT PER INTENTS")

        else:
            cur.execute("""
                UPDATE usuaris
                SET intents_fallits = %s
                WHERE username = %s
            """, (intents, username))

            registrar_log(username, "PASSWORD INCORRECTE")

        conn.commit()

    cur.close()
    conn.close()
    return None, None
    
#si falla 3 vegades bloqueja la compte.

#desbloquejar
def desbloquear_usuari(username):

    conn = psycopg2.connect(
        host="192.168.56.103",
        database="hospital",
        user="postgres",
        password="1234"
    )

    cur = conn.cursor()

    cur.execute("""
        UPDATE usuaris
        SET bloquejat = FALSE,
            intents_fallits = 0
        WHERE username = %s
    """, (username,))

    conn.commit()
    cur.close()
    conn.close()

    print("Usuari desbloquejat")
#desbloquear_usuari("admin")

#funció de tornar menú inicial
def tornar_login(win):
    win.destroy()

    from pantalles.login_window import iniciar_login
    iniciar_login()


