# minsky-machine

> *[English below](#english)*

---

## Español

Implementación de una máquina de registros de Minsky (equivalente Turing) con un IDE propio para la escritura, ejecución y depuración de programas. Pretende ser una herramienta pedagógica para el estudio de los fundamentos teóricos de la computación.

- **Máquina de registros**: En `minsky.py` se implementa una máquina de Minsky con N registros. Se definen las instrucciones de incremento `(i, +, j)` y decremento condicional `(i, -, j, k)`, así como la lectura y parsing del código fuente. Incluye un modo de ejecución normal y un modo de depuración paso a paso, con detección de bucles infinitos por límite de iteraciones.

- **IDE**: En `editor.py` se implementa un entorno de desarrollo integrado usando `tkinter`. Permite abrir, editar y guardar programas en formato `.txt`, ejecutarlos sobre la máquina y depurarlos con visualización del estado de los registros en cada iteración.

---

## English <a name="english"></a>

Implementation of a Minsky counter machine (Turing equivalent) with a custom IDE for writing, running, and debugging programs. It is intended as a pedagogical tool for the study of the theoretical foundations of computation.

- **Register machine**: `minsky.py` implements a Minsky machine with N registers. It defines increment instructions `(i, +, j)` and conditional decrement instructions `(i, -, j, k)`, along with source code reading and parsing. It includes a standard execution mode and a step-by-step debug mode, with infinite loop detection via an iteration limit.

- **IDE**: `editor.py` implements an integrated development environment using `tkinter`. It allows opening, editing, and saving programs in `.txt` format, running them on the machine, and debugging them with register state visualization at each iteration.
