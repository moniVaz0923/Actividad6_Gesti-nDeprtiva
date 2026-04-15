
class Jugador: 
    def __init__(self, nro_camiseta, apellido, posicion, minutos):
        # Atributos básicos definidos en la clase padre
        self.nro_camiseta = nro_camiseta
        self.apellido = apellido
        self.posicion = posicion
        self.minutos = minutos

    def obtener_resumen(self):
        return f"{self.apellido} (#{self.nro_camiseta}) - {self.posicion}"

# Aplicamos HERENCIA: Arquero hereda de Jugador
class Arquero(Jugador): 
    def __init__(self, nro_camiseta, apellido, minutos):
        # El arquero no registra goles según la consigna 
        super().__init__(nro_camiseta, apellido, "Arquero", minutos)

# Aplicamos HERENCIA para jugadores que sí marcan goles
class JugadorCampo(Jugador): 
    def __init__(self, nro_camiseta, apellido, posicion, minutos, goles):
        super().__init__(nro_camiseta, apellido, posicion, minutos)
        # ENCAPSULACIÓN: Atributo privado con doble guion bajo
        self.__goles = goles 

    # Método GET para acceder al valor privado desde afuera
    def get_goles(self): 
        return self.__goles
    
    # Método SET por si necesitás actualizar los goles después
    def set_goles(self, nuevos_goles):
        self.__goles = nuevos_goles
        