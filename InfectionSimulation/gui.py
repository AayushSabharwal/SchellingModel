import tkinter as tk
from tkinter import messagebox
from multiprocessing import Process, freeze_support
from static_visualization import static_run
from dynamic_visualization import dynamic_run
import simulation_parameters as params
from documentation import documentation as docs
import sys, asyncio

if sys.version_info[0]==3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class InfectionApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.winfo_toplevel().title('Infection Simulation')
        self.entries = {}
        self.active_process = None
        self.create_ui()

    def create_ui(self):
        self.create_horizontal_pair("Infection Radius", 1, 1)

        self.create_horizontal_pair("External Infection Chance", 1, 2)

        self.create_horizontal_pair("Mortality Rate", 1, 3)
        self.create_vertical_pair("Infection Duration Shape", 1, 4)
        self.create_vertical_pair("Infection Duration Scale", 2, 4)

        tk.Label(text="Has Recovery Immunity").grid(column=1, row=7)
        self.has_recovery_immunity = tk.IntVar()
        self.has_recovery_immunity_button = tk.Checkbutton(variable=self.has_recovery_immunity)
        self.has_recovery_immunity_button.grid(column=2, row=7)
        self.create_vertical_pair("Recovered Duration Shape", 1, 8)
        self.create_vertical_pair("Recovered Duration Scale", 2, 8)

        self.create_horizontal_pair("Vaccination Start", 1, 11)
        self.create_horizontal_pair("Newborn Vaccination Rate", 1, 12)
        self.create_horizontal_pair("General Vaccination Rate", 1, 13)

        self.create_vertical_pair("Mean Distance per Hour", 4, 1)
        self.create_vertical_pair("SD Distance per Hour", 5, 1)

        self.create_vertical_pair("Population Birth Rate", 4, 4)
        self.create_vertical_pair("Population Death Rate", 5, 4)

        self.create_vertical_pair("Grid Width", 4, 7)
        self.create_vertical_pair("Grid Height", 5, 7)

        self.create_horizontal_pair("Num Agents", 4, 9)
        self.create_horizontal_pair("Initial Infected Chance", 4, 11)
        tk.Label(text="Show Grid").grid(column=4, row=12)
        self.show_grid = tk.IntVar()
        self.show_grid_button = tk.Checkbutton(variable=self.show_grid)
        self.show_grid_button.grid(column=5, row=12)

        self.create_horizontal_pair("Max Iterations", 4, 13)

        tk.Label(text="Click on the parameter name for its description")\
            .grid(column=1, row=14, columnspan=5)

        self.dynamic_run_button = tk.Button(
            text="Dynamic Run", command=lambda: self.run_button(dynamic_run))
        self.dynamic_run_button.grid(column=1, row=15, columnspan=2)
        self.static_run_button = tk.Button(
            text="Static Run", command=lambda: self.run_button(static_run))
        self.static_run_button.grid(column=4, row=15, columnspan=2)
        self.kill_process_button = tk.Button(
            text="Stop Simulation", command=self.stop_current_simulation)
        self.kill_process_button.grid(column=3, row=15)
        self.update_entries()

    def create_horizontal_pair(self, name: str, col: int, row: int):
        entry_name = '_'.join(name.lower().split())
        tk.Button(text=name, bd=0,
                  command=lambda: messagebox.showinfo(name, docs[entry_name]))\
            .grid(column=col, row=row)
        self.entries[entry_name] = tk.Entry()
        self.entries[entry_name].grid(column=col + 1, row=row)

    def create_vertical_pair(self, name: str, col: int, row: int):
        entry_name = '_'.join(name.lower().split())
        tk.Button(text=name, bd=0,
                  command=lambda: messagebox.showinfo(name, docs[entry_name]))\
            .grid(column=col, row=row)
        self.entries[entry_name] = tk.Entry()
        self.entries[entry_name].grid(column=col, row=row + 1)

    def update_entries(self):
        for name, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, str(params.params[name]))
        self.show_grid.set(int(params.params['show_grid']))
        self.has_recovery_immunity.set(int(params.params['has_recovery_immunity']))

    def update_params(self):
        for name in params.params:
            if name in self.entries:
                try:
                    params.params[name] = type(params.params[name])(self.entries[name].get())
                except ValueError:
                    continue
        params.params["show_grid"] = bool(self.show_grid.get())
        params.params["has_recovery_immunity"] = bool(self.has_recovery_immunity.get())

    def stop_current_simulation(self):
        if self.active_process is not None:
            self.active_process.terminate()

    def run_button(self, command):
        self.update_params()
        params.sanity_check()
        self.stop_current_simulation()

        self.active_process = Process(target=command)
        self.active_process.start()


def on_quit():
    app.stop_current_simulation()
    root.destroy()

if __name__ == '__main__':
    freeze_support()
    root = tk.Tk()
    app = InfectionApp(root)
    root.protocol('WM_DELETE_WINDOW', on_quit)
    app.mainloop()