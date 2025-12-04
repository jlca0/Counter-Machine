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
            tipo (str): Un ainstrucción es tipo SUM si es de la forma (i,+,j) y es tipo RES si es de la forma (i,+,j,k). 

        Argumentos:
            tupla (tuple[int]): Una tupla de int que representa una instrucción, donde pone + ponemos +1 y donde pone - ponemos -1.
        """
        if len(tupla) == 3:
            self.registro = tupla[0] - 1
            self.estado_principal = tupla[2]
            self.estado_final = None
            self.tipo_instruccion = "SUM"
        elif len(tupla) == 4:
            self.registro = tupla[0] - 1
            self.estado_principal = tupla[2]
            self.estado_final = tupla[3]
            self.tipo_instruccion = "RES"

    def es_suma(self)->bool:
        """
        Comprueba si una instrucción es de tipo SUM o de tipo RES.
        """
        return self.estado_final is None


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
            self.Registro = np.zeros(N,dtype=int)  # Inicializamos los registros R1,...,RN con valor 0.
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
            registros_usados: (int) Número de registros que se usan en el código ejecutado o -1 que codifica un mensaje de error.
        """
        programa = self._leer(archivo)
        registros_usados = len(programa[0])
        self.Registro[:registros_usados] = np.array(list(programa[0]))
        estado_actual = 1
        iteraciones = 0

        while (estado_actual != 0 and iteraciones < self.iteraciones_maximas):
            instruccion = programa[estado_actual]
            if (instruccion.es_suma()):
                self.Registro[instruccion.registro] += 1
                estado_actual = instruccion.estado_principal
            else:
                if (self.Registro[instruccion.registro] > 0):
                    self.Registro[instruccion.registro] -= 1
                    estado_actual = instruccion.estado_principal
                else:
                    estado_actual = instruccion.estado_final
            iteraciones += 1

        if (iteraciones == self.iteraciones_maximas):  # Verificamos por qué acabó el bucle.
            return -1
        else:
            return registros_usados

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
            mensaje: (list[str]) Lista de mensajes de depurado mostrados en consola.
        """
        programa = self._leer(archivo)
        registros_usados = len(programa[0])
        self.Registro[:registros_usados] = np.array(list(programa[0]))
        estado_actual = 1
        iteraciones = 0
        mensaje = [f"Iteración  Estado  Registros \n",f"{iteraciones}          S{estado_actual}          {self.Registro[:registros_usados]} \n"]

        while (estado_actual != 0 and iteraciones < self.iteraciones_maximas):
            iteraciones += 1
            instruccion = programa[estado_actual]
            if (instruccion.es_suma()):
                self.Registro[instruccion.registro] += 1
                estado_actual = instruccion.estado_principal
            else:
                if (self.Registro[instruccion.registro] > 0):
                    self.Registro[instruccion.registro] -= 1
                    estado_actual = instruccion.estado_principal
                else:
                    estado_actual = instruccion.estado_final
            mensaje.append(f"{iteraciones}          S{estado_actual}          {self.Registro[:registros_usados]} \n")

        return mensaje

    def _leer(
            self, 
            archivo:str
        )->list[tuple[int] | Instruccion]:
        """
        Lee un archivo .txt conteniendo un programa y lo pasa a un string que comprende _ejecutar.

        Argumentos:
            archivo: (str) Contenido de un archivo de texto formateado como programa de máquina de resgistros.

        Salida: 
            programa: (list[tuple[int] | Instruccion]) Lista cuyos elementos son: programa[0] el estado inicial de la máquina (tuple[int]) y el resto instrucciones para una máquina de registros (Instruccion).
        """
        lineas = [l.strip() for l in archivo.split('\n') if l.strip()]  # Filter empty lines
        programa = []
    
        # Estado inicial de la máquina.
        valores = lineas[0].split(',')
        programa.append(tuple(int(x) for x in valores))
    
        # Las intrucciones del programa.
        for linea in lineas[1:]:
            valores = linea.split(',')
            programa.append(Instruccion(tuple(int(x) for x in valores)))
        return programa

