
class Jugador: 
    def __init__(self, nro_camiseta, apellido, posicion, minutos):
        self.nro_camiseta = str(nro_camiseta)
        self.apellido = str(apellido).capitalize()
        self.posicion = posicion
        self._minutos = int(minutos) if str(minutos).isdigit() else 0

    @property
    def minutos(self):
        return self._minutos

    @minutos.setter
    def minutos(self, valor):
        if int(valor) >= 0:
            self._minutos = int(valor)

    def obtener_resumen(self):
        return f"{self.apellido} (#{self.nro_camiseta}) - {self.posicion}"

class Arquero(Jugador): 
    def __init__(self, nro_camiseta, apellido, minutos):
        # Los arqueros no suman goles en este sistema
        super().__init__(nro_camiseta, apellido, "Arquero", minutos)

class JugadorCampo(Jugador): 
    def __init__(self, nro_camiseta, apellido, posicion, goles, minutos):
        super().__init__(nro_camiseta, apellido, posicion, minutos)
        self.__goles = int(goles) if str(goles).isdigit() else 0

    def get_goles(self): 
        return self.__goles
    
    def set_goles(self, nuevos_goles):
        if int(nuevos_goles) >= 0:
            self.__goles = int(nuevos_goles)
            