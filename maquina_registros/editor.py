import tkinter as tk
from tkinter import filedialog, scrolledtext

from minsky import Minsky


class Editor:
    def __init__(
        self, 
         N:int
    ) -> None:
        """
        Constructor de un objeto de la clase Editor que crea una ventana con un editor de programas
        para máquinas de registros con N registros.

        Atributos:
            ventana: (tk.Tk) Una ventana de la librería tkinter.
            N: (int) Número de registros que usa la máquina de registros con la que se va a trabajar.
            archivo: (str) Dirección del archivo al que tiene acceso el editor.
            texto: (tk.Text) Ventana de texto (editable).
            consola: (tk.Text) Ventana de texto (no editable).

        Argumentos:
            N (int): Número de registros que se van a usar.
        """
        self.ventana = tk.Tk()
        self.ventana.title("Editor Minsky")  # Creamos una ventana con nombre "Editor Minsky".
 
        self.N = N
        self.archivo = None  # La ruta de acceso del archivo de texto que vamos a editar.
        self._crear_interfaz()  # Método prvado que crea la interfaz.
        self.ventana.mainloop()  # Mostramos la pantalla.
    
    def _crear_interfaz(self)->None:
        """
        Método privado que configura los elementos que aparecen en la ventana "Editor Minsky".
        """        
        # Creamos los botones para navegar en el editor. 
        botones = tk.Frame(self.ventana)  # Agrupamos los botones en un solo frame.

        abrir = tk.Button(botones, text="Abrir", command=self._abrir)
        guardar = tk.Button(botones, text="Guardar", command=self._guardar)
        ejecutar = tk.Button(botones, text="Ejecutar", command=self._ejecutar)
        depurar = tk.Button(botones, text="Depurar", command=self._depurar)

        abrir.grid(row=0,column=0)  # Colocamos el botón en la posición (0,0) de botones.
        guardar.grid(row=0,column=1)
        ejecutar.grid(row=0,column=2)
        depurar.grid(row=0,column=3)

        botones.grid(row=0,column=0)  # Colocamos el frame botones dentro de ventana.

        # Creamos una ventana para el texto.
        self.texto = scrolledtext.ScrolledText(self.ventana, font=("Courier", 10), bg='grey', fg='blue')
        self.texto.grid(row=1, column=0)
        
        # Creamos una ventana para la consola.
        self.consola = scrolledtext.ScrolledText(self.ventana, font=("Courier", 9), state='disabled', bg='black', fg='white')
        self.consola.grid(row=2, column=0)
        
    
    def _abrir(self)->None:
        """
        Dada una ruta de acceso (que se guarda como atributo de Minsky) a un fichero .txt que se lee y se vuelca su
        contenido en la ventana de texto. Lo notificamos en la consola.
        """
        ruta = filedialog.askopenfilename(filetypes=[("Texto", "*.txt")])  # Seleccionamos una ruta de acceso.
        if ruta:
            fichero = open(ruta, 'r').read()
            self.texto.delete(1.0, tk.END)  # Borramos el texto que mostraba el editor.
            self.texto.insert(1.0, fichero) # Volcamos el nuevo archivo.
            self.archivo = ruta  
            self._escribir(f"Archivo cargado: {ruta}")
    
    def _guardar(self)->None:
        """
        Dada una ruta de acceso guarda el texto en pantalla en el fichero de texto abierto o en uno nuevo
        si es el caso.
        """
        if not self.archivo:  # No se ha abierto ningún fichero.
            self.archivo = filedialog.asksaveasfilename(filetypes=[("Texto", "*.txt")])  # Seleccionamos una dirección de guardado.
        else:
            open(self.archivo, 'w').write(self.texto.get(1.0, tk.END))  # Se sobreescribe el fichero.
        self._escribir(f"Guardado: {self.archivo} \n")
    
    def _ejecutar(self)->None:        
        """
        Seleccionado un archivo de texto en el editor se ejecuta el programa usando un objeto de clase
        Minsky, imprime en consola el resultado.
        """
        
        # Ejecutamos el programa seleccionado con esos valores usando un objeto de clase Minsky.
        maquina = Minsky(self.N)
        registros_usados = maquina.ejecutar(self.texto.get("1.0", tk.END))

        # Pintamos el proceso en pantalla.
        self.consola.config(state='normal')
        self.consola.delete(1.0, tk.END)
        self.consola.config(state='disabled')
        self._escribir(f"Ejecutando: {self.archivo}...")

        if (registros_usados > 0):  # Minsky.ejecutar devolvía -1 si el programa no terminaba.
            self._escribir(f"Estado final: {maquina.Registro[:registros_usados]} \n")
        else:
            self._escribir(f"El programa no termina, número máximo de iteraciones alcanzado {maquina.iter_max}")

    def _depurar(self)->None:
        """
        Seleccionado un archivo de texto en el editor se ejecuta el programa paso a paso 
        usando un objeto de clase Minsky.
        """
        maquina = Minsky(self.N)
        mensaje = maquina.depurar(self.texto.get("1.0",tk.END))

        self.consola.config(state='normal')
        self.consola.delete(1.0, tk.END)
        self.consola.config(state='disabled')
        for linea in reversed(mensaje):
            self._escribir(linea)
        self._escribir(f"Depurando: {self.archivo}... \n")  #No distinguimos porque Minsky.depurar siempre devuelve todo, para verificar mal funcionamiento.
        
    def _escribir(
            self, 
            mensaje:str
        )->None:
        """
        Dado un mensaje (interno) lo pinta en la consola.

        Atributos:
            mensaje (string): El mensaje que queremos mostrar.
        """
        self.consola.config(state='normal')
        self.consola.insert(1.0,mensaje)
        self.consola.config(state='disabled')

if __name__ == "__main__":
    editor = Editor(100)
