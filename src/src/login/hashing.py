#seguretat de contrasenyes amb bcrypt
import bcrypt

def generar_hash(password):
    """
    Convierte contraseña en hash seguro
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verificar_password(password, hash_guardado):
    """
    Verifica contraseña introducida
    """
    return bcrypt.checkpw(password.encode(), hash_guardado.encode())

