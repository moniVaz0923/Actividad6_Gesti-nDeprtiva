import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        return mysql.connector.connect(
            host="b4lztfalbfsjjzaecdm2-mysql.services.clever-cloud.com",
            user="ujqgj2ndghsaiu51", 
            password="obKgetgQt2hlY02Tlj2D", 
            database="b4lztfalbfsjjzaecdm2",
            port=3306,
            autocommit=True 
        )
    except Error as e:
        print(f"Error crítico de conexión: {e}")
        return None

def guardar_jugador(j):
    conn = conectar()
    if not conn: return False
    try:
        cursor = conn.cursor()
        # Verificamos si tiene el método get_goles (Encapsulamiento del Código )
        goles = j.get_goles() if hasattr(j, 'get_goles') else 0
        
        sql = """
            INSERT INTO jugadores (nro_camiseta, apellido, posicion, minutos, goles) 
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            apellido = VALUES(apellido), 
            posicion = VALUES(posicion), 
            minutos = VALUES(minutos), 
            goles = VALUES(goles)
        """        
        
        cursor.execute(sql, (j.nro_camiseta, j.apellido, j.posicion, j.minutos, goles))
        conn.close()
        return True
    except Error as err:
        print(f"Error al guardar: {err}")
        return False
    
def guardar_jugador(j):
    conn = conectar()
    if not conn: return False
    try:
        cursor = conn.cursor()
        
        # MODIFICADO: Extraemos los valores explícitamente para evitar confusiones
        goles_a_guardar = j.get_goles() if hasattr(j, 'get_goles') else 0
        minutos_a_guardar = j.minutos
        
        # MODIFICADO: Sentencia SQL con orden estricto (Goles primero, luego Minutos)
        # Usamos ON DUPLICATE KEY UPDATE para evitar los duplicados que mencionaste antes
        sql = """
            INSERT INTO jugadores (nro_camiseta, apellido, posicion, goles, minutos) 
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            apellido = VALUES(apellido), 
            posicion = VALUES(posicion), 
            goles = VALUES(goles), 
            minutos = VALUES(minutos)
        """
        
        # MODIFICADO: Los valores aquí DEBEN seguir el mismo orden que arriba (Goles, luego Minutos)
        datos = (j.nro_camiseta, j.apellido, j.posicion, goles_a_guardar, minutos_a_guardar)
        
        cursor.execute(sql, datos)
        conn.close()
        return True
    except Error as err:
        print(f"Error al guardar: {err}")
        return False

def obtener_todos():
    con = conectar()
    if con:
        cursor = con.cursor()
        # MODIFICADO: Aseguramos el orden de salida para la tabla de la App
        # El orden debe ser: Apellido, N°, Posición, Goles, Minutos
        cursor.execute("SELECT apellido, nro_camiseta, posicion, goles, minutos FROM jugadores ORDER BY apellido ASC")
        jugadores = cursor.fetchall()
        con.close()
        return jugadores
    return []

def buscar_por_camiseta(numero):
    con = conectar()
    if con:
        cursor = con.cursor()
        query = "SELECT apellido, nro_camiseta, posicion, goles, minutos FROM jugadores WHERE nro_camiseta = %s"
        cursor.execute(query, (numero,))
        resultado = cursor.fetchall()
        con.close()
        return resultado
    return []

def actualizar_estadistica(camiseta, tipo, valor):
    """Suma goles o minutos al jugador existente"""
    con = conectar()
    if con:
        try:
            cursor = con.cursor()
            # Usamos F-string solo para el nombre de la columna, el valor va por parámetro por SEGURIDAD
            query = f"UPDATE jugadores SET {tipo} = {tipo} + %s WHERE nro_camiseta = %s"
            cursor.execute(query, (valor, camiseta))
            con.close()
            return True
        except Error as e:
            print(f"Error al actualizar estadística: {e}")
    return False

def actualizar_jugador_completo(camiseta, nuevo_apellido, nueva_posicion):
    """Permite corregir errores de carga de datos básicos"""
    con = conectar()
    if con:
        try:
            cursor = con.cursor()
            query = "UPDATE jugadores SET apellido = %s, posicion = %s WHERE nro_camiseta = %s"
            cursor.execute(query, (nuevo_apellido, nueva_posicion, camiseta))
            con.close()
            return True
        except Error as e:
            print(f"Error al modificar jugador: {e}")
    return False

def eliminar_jugador_db(camiseta):
    con = conectar()
    if con:
        try:
            cursor = con.cursor()
            query = "DELETE FROM jugadores WHERE nro_camiseta = %s"
            cursor.execute(query, (camiseta,))
            con.close()
            return True
        except Error as e:
            print(f"Error al eliminar: {e}")
            return False
    return False
