import numpy as np


class Instruction:
    def __init__(
            self, 
            x:tuple[int]
        )->None:
        """
        Creates an object of the class Instruction which resembles a counter machine instruction.

        Atributes:
            register (int): register edited by the instruction.
            main_state (int): State reached by the machine after the execution of the instruction.
            final_state (Optional[int]): Final state reached after the execution of a RES type of Instruction.

        Arguments:
            x (tuple[int]): An int tuple which resembles an instruction, we match the usual plus, minus symbols with +1 and -1 respectively.
        """
        if len(x) == 3:
            self.register = x[0] - 1
            self.main_state = x[2]
            self.final_state = None
        elif len(x) == 4:
            self.register = x[0] - 1
            self.main_state = x[2]
            self.final_state = x[3]

    def is_sum(self)->bool:
        """
        Checks whether an instruction is of the type (i,+,j).
        """
        return self.final_state is None

    def is_res(self)->bool:
        """
        Checks whether an instruction is of the type (i,-,j,k).
        """
        return self.final_state is not None

class Program:
    def __init__(
            self,
            x:list[tuple[int] | Instruction]
        )->None:
        """
        Creates an obect of the class Program which contains all the information about the initial state of the machine,
        the number of registres used as well as the instruction related to each state.

        Atributes:
            initial_state: (tuple[int]) A tuple containing the registres used by the program that will be run.
            number_registres: (int) The number of registres used.
            instructions: list[Instruction]  A list containing each instruction holding the position corresponding to its related state, 
            we make None correspond to the default final state S0.

        Arguments:
            x: (list[tuple[int] | Registro]) A list whose first element is a tuple itself containing the used registers, 
            the rest of the elements correspond to the instructions of the program.
        """
        self.initial_state = x[0]
        self.number_registers = len(x[0])
        self.instructions = [None] + x[1:]
    
    def get_instruction(
        self,
        state:int
        )->Instruction:
        """
        Given a state it gets the instruction related to that state of the machine.
        """
        return self.instructions[state]
    

class Minsky:
    def __init__(
            self, 
            N:int
        )->None:
        """
        Creates an object of class Minsky which recreates a counter machine.
        Atributes:
            register: (array[int]) Value of each register of the Minsky machine.
            max_iterations: (int) Maximum number of iterations.

        Arguments:
            N (int): Number of registers to be used.
        """
        self.max_iterations = int(1e8)  # Maximun number of iterations for handling of infinite loops.
        if N > 0:
            self.register = np.zeros(N, dtype=int)  # Initializes registers R1,...,RN to 0.
        else:
            raise ValueError("A natural number of registers is expected (N)")

    def run(
            self, 
            file:str
        )->int:
        """
        Runs a given program on the counter machine.

        Arguments:
            file: (str) Content of text file properly formated as counter machine source code.

        Returns:
            number_registers: (int) Number of registers used by the program running or -1, which codifies a error message for the editor.
        """
        program = self._read_program(file)
        self.register[:program.number_registers] = np.array(program.initial_state, dtype=int)
        current_state = 1
        iterations = 0

        while current_state != 0 and iterations < self.max_iterations:
            instruction = program.get_instruction(current_state)
            if instruction.is_sum():
                self.register[instruction.register] += 1
                current_state = instruction.main_state
            elif instruction.is_res():
                if self.register[instruction.register] > 0:
                    self.register[instruction.register] -= 1
                    current_state = instruction.main_state
                else:
                    current_state = instruction.final_state
            iterations += 1

        if iterations == self.max_iterations:  # Chekcs why the loop finalized.
            return -1
        else:
            return program.number_registers

    def debug(
            self, 
            file:str
        )->list[str]:
        """
        Runs a given program on the counter machine and saves in a list the state of the machine 
        and the value of its registers on each iteration.

        Arguments:
            file: (str) Content of text file properly formated as counter machine source code.

        Returns:
            history: (list[str]) List of debugging messages to be printed on the terminal.
        """
        program = self._read_program(file)
        self.register[:program.number_registers] = np.array(program.initial_state, dtype=int)
        current_state = 1
        iterations = 0
        history = [f"Iteration  State  Registers \n",f"{iterations}          S{current_state}          {self.register[:program.number_registers]} \n"]

        while current_state != 0 and iterations < self.max_iterations:
            iterations += 1
            instruction = program.get_instruction(current_state)
            if instruction.is_sum():
                self.register[instruction.register] += 1
                current_state = instruction.main_state
            elif instruction.is_res():
                if self.register[instruction.register] > 0:
                    self.register[instruction.register] -= 1
                    current_state = instruction.main_state
                else:
                    current_state = instruction.final_state
            history.append(f"{iterations}          S{current_state}          {self.register[:program.number_registers]} \n")

        return history

    def _read_program(
            self, 
            file:str
        )->Program:
        """
        Reads a txt file containing a program and returns a string for Minsky.run.

        Arguments:
            file: (str) Content of text file properly formated as counter machine source code.

        Returns: 
            program: (Program.) A Program object.
        """
        lines = [l.strip() for l in file.split('\n') if l.strip()]  # Filter empty lines
        file_content = []
    
        # Estado inicial de la máquina.
        values = lines[0].split(',')
        file_content.append(tuple(int(x) for x in values))
    
        # Las intrucciones del programa.
        for line in lines[1:]:
            values = line.split(',')
            file_content.append(Instruction(tuple(int(x) for x in values)))

        return Program(file_content)
