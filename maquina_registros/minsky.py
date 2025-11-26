import numpy as np


class Minsky:
    def __init__(
            self, 
            N:int
        )->None:
        """
        Construye un objeto de la clase Minsky que simula una máquina de registros.

        Atributos:
            Registro: (array[int]) Valor de cada registro de la máquina de Minsky.

        Argumentos:
            N (int): Número de registros que se van a usar.
        """
        self.Registro = np.zeros(N,dtype=int)  # Inicializamos los registros R1,...,RN con valor 0.

    def ejecutar(
            self, 
            archivo:str
        )->int:
        """
        Ejecuta un programa dado usando la máquina de registros.

        Argumentos:
            archivo: (str) Contenido de un archivo de texto formateado como programa de máquina de resgistros.

        Salida:
            numero_registros: (int) Número de registros que se usan en el código ejecutado.
        """
        programa = self._leer(archivo)
        numero_registros = len(programa[0])
        self.Registro[:numero_registros] = np.array(list(programa[0]))
        Estado = 1
        while (Estado != 0):
            if (len(programa[Estado]) == 3):  # Instrucción del tipo (i,+,j)
                self.Registro[programa[Estado][0]-1] += 1
                Estado = programa[Estado][2]
            else:  #Instrucción del tipo (i,-,j,k)
                if (self.Registro[programa[Estado][0]-1] > 0):
                    self.Registro[programa[Estado][0]-1] -= 1
                    Estado = programa[Estado][2]
                else:
                    Estado = programa[Estado][3]
        return numero_registros 

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
            numero_registros: (list[str]) Lista de mensajes de depurado mostrados en consola.
        """
        programa = self._leer(archivo)
        numero_registros = len(programa[0])
        self.Registro[:numero_registros] = np.array(list(programa[0]))
        Estado = 1
        contador = 0
        mensaje = [f"Iteración  Estado  Registros \n",f"{contador}          S{Estado}          {self.Registro[:numero_registros]} \n"]
        while (Estado != 0):
            contador += 1
            if (len(programa[Estado]) == 3):  # Instrucción del tipo (i,+,j)
                self.Registro[programa[Estado][0]-1] += 1
                Estado = programa[Estado][2]
            else:  #Instrucción del tipo (i,-,j,k)
                if (self.Registro[programa[Estado][0]-1] > 0):
                    self.Registro[programa[Estado][0]-1] -= 1
                    Estado = programa[Estado][2]
                else:
                    Estado = programa[Estado][3]
            mensaje.append(f"{contador}          S{Estado}          {self.Registro[:numero_registros]} \n")
        return mensaje

    def _leer(
            self, 
            archivo:str
        )->list[tuple[int]]:
        """
        Lee un archivo .txt conteniendo un programa y lo pasa a un string que comprende _ejecutar.

        Argumentos:
            archivo: (str) Contenido de un archivo de texto formateado como programa de máquina de resgistros.

        Salida: 
            programa: (list[tuple[int]]) Lista cuyos elementos son instrucciones para una máquina de registros.
        """
        lineas = archivo.split('\n')
        programa = []
        for linea in lineas:
            linea_limpia = linea.strip()          
            if linea_limpia:
                instruccion_lista = linea_limpia.split(',')
                programa.append(tuple(int(x) for x in instruccion_lista))
        return programa

