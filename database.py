import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="b4lztfalbfsjjzaecdm2-mysql.services.clever-cloud.com",
        user="ujqgj2ndghsaiu51", 
        password="obKgetgQt2hlY02Tlj2D", 
        database="b4lztfalbfsjjzaecdm2",
        port=3306,
        autocommit=True 
    )

def guardar_jugador(j):
    try:
        conn = conectar()
        cursor = conn.cursor()
        # Verificamos si es Arquero o JugadorCampo para los goles
        goles = j.get_goles() if hasattr(j, 'get_goles') else 0
        
        sql = "INSERT INTO jugadores (nro_camiseta, apellido, posicion, minutos, goles) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (j.nro_camiseta, j.apellido, j.posicion, j.minutos, goles))
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al guardar en la base de datos: {err}")
        return False

def obtener_todos():
    """Trae a todos los jugadores para llenar la tabla al iniciar"""
    con = conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("SELECT apellido, nro_camiseta, posicion, goles, minutos FROM jugadores")
        jugadores = cursor.fetchall()
        con.close()
        return jugadores
    return []

def buscar_por_camiseta(numero):
    """Busca un jugador específico por su número de camiseta"""
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
    """Suma goles o minutos al jugador"""
    con = conectar()
    if con:
        cursor = con.cursor()
        # 'tipo' será la columna (goles o minutos)
        query = f"UPDATE jugadores SET {tipo} = {tipo} + %s WHERE nro_camiseta = %s"
        cursor.execute(query, (valor, camiseta))
        con.commit()
        con.close()
        return True
    return False

# --- ESTA ES LA FUNCIÓN QUE FALTABA ---
def actualizar_jugador_completo(camiseta, nuevo_apellido, nueva_posicion):
    """Actualiza los datos básicos de un jugador ya registrado"""
    con = conectar()
    if con:
        try:
            cursor = con.cursor()
            query = "UPDATE jugadores SET apellido = %s, posicion = %s WHERE nro_camiseta = %s"
            cursor.execute(query, (nuevo_apellido, nueva_posicion, camiseta))
            con.commit()
            con.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error al actualizar: {err}")
            return False
    return False

def eliminar_jugador_db(camiseta):
    """Elimina un jugador de la base de datos"""
    con = conectar()
    if con:
        try:
            cursor = con.cursor()
            query = "DELETE FROM jugadores WHERE nro_camiseta = %s"
            cursor.execute(query, (camiseta,))
            con.commit()
            con.close()
            return True
        except:
            return False
    return False