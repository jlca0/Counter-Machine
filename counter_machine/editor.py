import tkinter as tk
from tkinter import filedialog, scrolledtext

from minsky import Minsky


class Editor:
    def __init__(
        self, 
         N:int
    ) -> None:
        """
        Creates an Editor object which opens an IDE for a counter machine with N registers.

        Attributes:
            window: (tk.Tk) A window from the tkinter library.
            N: (int) Number of registers of the counter machine.
            current_file: (str) Path to the source code file being edited.
            text: (tk.Text) Text window (writing enabled)
            terminal: (tk.Text) Text window (writing disabled).

        Arguments:
            N (int): Number of registers of the counter machine.
        """
        self.window = tk.Tk()
        self.window.title("Minsky IDE")  # Opens a window titled Minsky IDE.
 
        self.N = N
        self.current_file = None
        self._open_IDE()
        self.window.mainloop()
    
    def _open_IDE(self)->None:
        """
        Private method which configures the Minsky IDE window.
        """        
        # Buttons for navigating the IDE.
        buttons = tk.Frame(self.window)  # Stacks the buttons in a single frame.

        open = tk.Button(buttons, text="Open", command=self._open)
        save = tk.Button(buttons, text="Save", command=self._save)
        run = tk.Button(buttons, text="Run", command=self._run)
        debug = tk.Button(buttons, text="Debug", command=self._debug)

        open.grid(row=0,column=0)  # Places the button to the position (0,0).
        save.grid(row=0,column=1)
        run.grid(row=0,column=2)
        debug.grid(row=0,column=3)

        buttons.grid(row=0,column=0)  # Places the frame within the window.

        # A scrollable text window for the text editor.
        self.text = scrolledtext.ScrolledText(self.window, font=("Courier", 10), bg='grey', fg='blue')
        self.text.grid(row=1, column=0)
        
        # A scrollable text window for the terminal.
        self.terminal = scrolledtext.ScrolledText(self.window, font=("Courier", 9), state='disabled', bg='black', fg='white')
        self.terminal.grid(row=2, column=0)
        
    
    def _open(self)->None:
        """
        Given a txt file path it reads it and shows it, both in the text window and the terminal.
        """
        path = filedialog.askopenfilename(filetypes=[("Texto", "*.txt")])  # Selects a file path.
        if path:
            file = open(path, 'r').read()
            self.text.delete(1.0, tk.END)
            self.text.insert(1.0, file)
            self.current_file = path  
            self._write_terminal(f"Open: {path}")
    
    def _save(self)->None:
        """
        Given a txt file path it saves the text window to the current file being edited (overwriting it) 
        or to a new file whenever needed.
        """
        if not self.current_file:  # No file was being edited.
            self.current_file = filedialog.asksaveasfilename(filetypes=[("Texto", "*.txt")])  # Selects a saving path.
        else:
            open(self.current_file, 'w').write(self.text.get(1.0, tk.END))  # Overwrites the file.
        self._write_terminal(f"Saved: {self.current_file} \n")
    
    def _run(self)->None:        
        """
        Once a file is selected and shown on the text window it runs it on the counter machine, 
        printing the result on the terminal.
        """
        
        # Runs the selected program
        machine = Minsky(self.N)
        registers_used = machine.run(self.text.get("1.0", tk.END))

        # We give notice on scren.
        self._delete_terminal()
        self._write_terminal(f"Running: {self.current_file}...")

        if (registers_used > 0):  # Minsky.runs returned -1 in case of an infinite loop.
            self._write_terminal(f"Final state: {machine.register[:registers_used]} \n")
        else:
            self._write_terminal(f"The program does not stop, maximum number of iterations reached {machine.max_iterations}")

    def _debug(self)->None:
        """
        Once a file is selected and shown on screen it is run step by step on the counter machine.
        """
        machine = Minsky(self.N)
        message = machine.debug(self.text.get("1.0",tk.END))

        self._delete_terminal()
        for line in reversed(message):
            self._write_terminal(line)
        self._write_terminal(f"Debugging: {self.current_file}... \n")  #Just one case, since we want to show every single iteration.
        
    def _write_terminal(
            self, 
            message:str
        )->None:
        """
        Given a message it is printed on the terminal.

        Attributes:
            message (string): The message to be printed.
        """
        self.terminal.config(state='normal')
        self.terminal.insert(1.0,message)
        self.terminal.config(state='disabled')

    def _delete_terminal(self)->None:
        """
        Deletes the content of the terminal.
        """
        self.terminal.config(state='normal')
        self.terminal.delete(1.0, tk.END)
        self.terminal.config(state='disabled')

if __name__ == "__main__":
    editor = Editor(100)
