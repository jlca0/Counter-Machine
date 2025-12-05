import numpy as np


class Instruccion:
    def __init__(
            self, 
            tupla:tuple[int]
        )->None:
        """
        Construye un objeto de clase Instruccion que simula una instrucción para una máquina de registros.

        Atributos:
            registro (int): Registro que edita la instrucción.
            estado_principal (int): Estado que adopta la máquina si la instrucción consigue modificar un registro.
            estado_final (Optional[int]): Estado final que alcanza una instrucción del tipo RES.

        Argumentos:
            tupla (tuple[int]): Una tupla de int que representa una instrucción, donde pone + ponemos +1 y donde pone - ponemos -1.
        """
        if len(tupla) == 3:
            self.registro = tupla[0] - 1
            self.estado_principal = tupla[2]
            self.estado_final = None
        elif len(tupla) == 4:
            self.registro = tupla[0] - 1
            self.estado_principal = tupla[2]
            self.estado_final = tupla[3]

    def es_suma(self)->bool:
        """
        Comprueba si una instrucción es de tipo (i,+,j).
        """
        return self.estado_final is None

    def es_resta(self)->bool:
        """
        Comprueba si una instrucción es de tipo (i,-,j,k).
        """
        return self.estado_final is not None

class Programa:
    def __init__(
            self,
            lista:list[tuple[int] | Instruccion]
        )->None:
        """
        Crea un objeto de la clase Programa que contiene la información sobre el estado inicial de la máquina, 
        el número de registros usados y las instrucciones asociadas a cada estado.

        Atributos:
            estado_inicial: (tuple[int]) Una tupla conteniendo los registros usados por el programa a ejecutar.
            numero_registros: (int) El número de registros usados.
            instrucciones: list[Instruccion] Una lista con cada instrucción en la posición correspondiente a su estado, 
            al S0 le hacemos corresponder None.

        Argumentos:
            lista: (list[tuple[int] | Registro]) Una lista cuyo primer elemento es la tupla con los registros usados 
            y el resto de elementos se corresponden a las instrucciones del programa.
        """
        self.estado_inicial = lista[0]
        self.numero_registros = len(lista[0])
        self.instrucciones = [None] + lista[1:]
    
    def obtener_instruccion(
        self,
        estado:int
        )->Instruccion:
        """
        Dado un estado accede a la instrucción asociada en el programa.
        """
        return self.instrucciones[estado]
    

class Minsky:
    def __init__(
            self, 
            N:int
        )->None:
        """
        Construye un objeto de la clase Minsky que simula una máquina de registros.

        Atributos:
            Registro: (array[int]) Valor de cada registro de la máquina de Minsky.
            iteraciones_maximas: (int) Número máximo de iteraciones.

        Argumentos:
            N (int): Número de registros que se van a usar.
        """
        self.iteraciones_maximas = int(1e8)  # Número máximo de iteraciones, gestionamos bucles infinitos.
        if N > 0:
            self.registro = np.zeros(N, dtype=int)  # Inicializamos los registros R1,...,RN con valor 0.
        else:
            raise ValueError("Debe introducirse un número natural de registros disponibles (N)")

    def ejecutar(
            self, 
            archivo:str
        )->int:
        """
        Ejecuta un programa dado usando la máquina de registros.

        Argumentos:
            archivo: (str) Contenido de un archivo de texto formateado como programa de máquina de resgistros.

        Salida:
            numero_registros: (int) Número de registros que se usan en el código ejecutado o -1 que codifica un mensaje de error.
        """
        programa = self._leer_programa(archivo)
        self.registro[:programa.numero_registros] = np.array(programa.estado_inicial, dtype=int)
        estado_actual = 1
        iteraciones = 0

        while estado_actual != 0 and iteraciones < self.iteraciones_maximas:
            instruccion = programa.obtener_instruccion(estado_actual)
            if instruccion.es_suma():
                self.registro[instruccion.registro] += 1
                estado_actual = instruccion.estado_principal
            elif instruccion.es_resta():
                if self.registro[instruccion.registro] > 0:
                    self.registro[instruccion.registro] -= 1
                    estado_actual = instruccion.estado_principal
                else:
                    estado_actual = instruccion.estado_final
            iteraciones += 1

        if iteraciones == self.iteraciones_maximas:  # Verificamos por qué acabó el bucle.
            return -1
        else:
            return programa.numero_registros

    def depurar(
            self, 
            archivo:str
        )->list[str]:
        """
        Ejecuta un programa dado usando la máquina de registros y almacena en una lista 
        el estado de la máquina y los registros en cada iteración.

        Argumentos:
            archivo: (str) Contenido de un archivo de texto formateado como programa de máquina de resgistros.

        Salida:
            historial: (list[str]) Lista de mensajes de depurado mostrados en consola.
        """
        programa = self._leer_programa(archivo)
        self.registro[:programa.numero_registros] = np.array(programa.estado_inicial, dtype=int)
        estado_actual = 1
        iteraciones = 0
        historial = [f"Iteración  Estado  Registros \n",f"{iteraciones}          S{estado_actual}          {self.registro[:programa.numero_registros]} \n"]

        while estado_actual != 0 and iteraciones < self.iteraciones_maximas:
            iteraciones += 1
            instruccion = programa.obtener_instruccion(estado_actual)
            if instruccion.es_suma():
                self.registro[instruccion.registro] += 1
                estado_actual = instruccion.estado_principal
            elif instruccion.es_resta():
                if self.registro[instruccion.registro] > 0:
                    self.registro[instruccion.registro] -= 1
                    estado_actual = instruccion.estado_principal
                else:
                    estado_actual = instruccion.estado_final
            historial.append(f"{iteraciones}          S{estado_actual}          {self.registro[:programa.numero_registros]} \n")

        return historial

    def _leer_programa(
            self, 
            archivo:str
        )->Programa:
        """
        Lee un archivo .txt conteniendo un programa y lo pasa a un string que comprende _ejecutar.

        Argumentos:
            archivo: (str) Contenido de un archivo de texto formateado como programa de máquina de resgistros.

        Salida: 
            programa: (Programa) Un objeto del tipo Programa.
        """
        lineas = [l.strip() for l in archivo.split('\n') if l.strip()]  # Filter empty lines
        contenido_archivo = []
    
        # Estado inicial de la máquina.
        valores = lineas[0].split(',')
        contenido_archivo.append(tuple(int(x) for x in valores))
    
        # Las intrucciones del programa.
        for linea in lineas[1:]:
            valores = linea.split(',')
            contenido_archivo.append(Instruccion(tuple(int(x) for x in valores)))

        return Programa(contenido_archivo)
