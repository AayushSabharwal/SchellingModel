import sys
import asyncio
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from multiprocessing import Process, Manager, freeze_support
try:
    from static_run import static_run
    from dynamic_run import dynamic_run
    from documentation import documentation as docs
    from simulation_parameters import DEFAULT_PARAMS, sanity_check
except ImportError:
    from InfectionSimulation.static_run import static_run
    from InfectionSimulation.dynamic_run import dynamic_run
    from InfectionSimulation.documentation import documentation as docs
    from InfectionSimulation.simulation_parameters import DEFAULT_PARAMS, sanity_check

if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class InfectionApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.winfo_toplevel().title('Infection Simulation')
        self.entries = {}
        self.active_process = None
        self.available_row = 0
        self.params = Manager().dict(DEFAULT_PARAMS)
        self.create_ui()

    def create_ui(self):
        self.create_vertical_pair("Infection Radius", 1, False)
        self.create_vertical_pair("Mortality Rate", 2, False)

        self.create_vertical_pair("Infection Duration Shape", 4, False)
        self.create_vertical_pair("Infection Duration Scale", 5)

        self.create_documentation_button("Infection Chance Function")\
            .grid(column=1, row=self.available_row)
        self.available_row += 1
        self.infection_chance_function = tk.Text(self.master, width=1, height=3)
        self.infection_chance_function.grid(row=self.available_row, column=1, columnspan=5,
                                            sticky='ew', padx=14)
        self.available_row += 1

        self.create_separator()

        self.create_horizontal_pair("Initial Infected Chance", 1, False)
        self.create_horizontal_pair("External Infection Chance", 4)

        self.create_documentation_button("Has Recovery Immunity")\
            .grid(column=1, row=self.available_row)
        self.has_recovery_immunity = tk.IntVar()
        tk.Checkbutton(self.master, variable=self.has_recovery_immunity)\
            .grid(column=2, row=self.available_row)

        self.create_horizontal_pair("Vaccination Start", 4)
        self.create_vertical_pair("Recovered Duration Shape", 1, False)
        self.create_vertical_pair("Recovered Duration Scale", 2, False)

        self.create_vertical_pair("Newborn Vaccination Rate", 4, False)
        self.create_vertical_pair("General Vaccination Rate", 5)

        self.create_vertical_pair("Mean Distance Per Hour", 1, False)
        self.create_vertical_pair("SD Distance Per Hour", 2, False)

        self.create_vertical_pair("Population Birth Rate", 4, False)
        self.create_vertical_pair("Population Death Rate", 5)

        self.create_separator()

        self.create_documentation_button("Show Grid").grid(column=1, row=self.available_row)
        self.show_grid = tk.IntVar()
        tk.Checkbutton(self.master, variable=self.show_grid).grid(column=2, row=self.available_row)

        self.create_horizontal_pair("Num Agents", 4)

        self.create_vertical_pair("Grid Width", 1, False)
        self.create_vertical_pair("Grid Height", 2, False)

        self.create_horizontal_pair("Data Collection Frequency", 4)
        self.create_horizontal_pair("Max Iterations", 4)
        self.update_entries()
        self.update_params()

        tk.Label(self.master, text="Click on parameter name for its description")\
            .grid(column=1, row=self.available_row, columnspan=5)
        self.available_row += 1
        tk.Label(self.master, text="Always run Stop Simulation before changing any parameters")\
            .grid(column=1, row=self.available_row, columnspan=5)
        self.available_row += 1

        tk.Button(text="Dynamic Run", command=lambda: self.run_button(dynamic_run))\
            .grid(column=1, row=self.available_row, columnspan=2)
        tk.Button(text="Stop Simulation", command=self.stop_current_simulation)\
            .grid(column=3, row=self.available_row)
        tk.Button(text="Static Run", command=lambda: self.run_button(static_run))\
            .grid(column=4, row=self.available_row, columnspan=2)
        self.configure_grid()

    def create_horizontal_pair(self, name: str, col: int, increment_row: bool = True):
        entry_name = '_'.join(name.lower().split())
        self.create_documentation_button(name).grid(column=col, row=self.available_row)
        self.entries[entry_name] = tk.Entry()
        self.entries[entry_name].grid(column=col + 1, row=self.available_row)
        if increment_row:
            self.available_row += 1

    def create_vertical_pair(self, name: str, col: int, increment_row: bool = True):
        entry_name = '_'.join(name.lower().split())
        self.create_documentation_button(name).grid(column=col, row=self.available_row)
        self.entries[entry_name] = tk.Entry()
        self.entries[entry_name].grid(column=col, row=self.available_row + 1)
        if increment_row:
            self.available_row += 2

    def create_documentation_button(self, name: str):
        entry_name = '_'.join(name.lower().split())
        return tk.Button(self.master, text=name, bd=0,
                         command=lambda: messagebox.showinfo(name, docs[entry_name]))

    def create_separator(self, orient=tk.HORIZONTAL):
        ttk.Separator(self.master, orient=orient).grid(column=1, row=self.available_row,
                                                       columnspan=5, sticky='nsew',
                                                       padx=14, pady=10)
        self.available_row += 1

    def update_entries(self):
        for name, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, str(self.params[name]))
        self.show_grid.set(int(self.params['show_grid']))
        self.has_recovery_immunity.set(int(self.params['has_recovery_immunity']))
        self.infection_chance_function.delete(0., tk.END)
        self.infection_chance_function.insert(0., str(self.params['infection_chance_function']))

    def update_params(self):
        for name in self.params:
            if name in self.entries:
                try:
                    self.params[name] = type(self.params[name])(self.entries[name].get())
                except ValueError:
                    continue
        self.params["show_grid"] = bool(self.show_grid.get())
        self.params["has_recovery_immunity"] = bool(self.has_recovery_immunity.get())
        self.params['infection_chance_function'] = 'lambda dist: ' + self.infection_chance_function.get(0., tk.END)

    def stop_current_simulation(self):
        if self.active_process is not None:
            self.active_process.terminate()

    def run_button(self, command):
        self.update_params()
        sanity_check(self.params)
        self.stop_current_simulation()

        self.active_process = Process(target=command, args=(self.params, ))
        self.active_process.start()

    def configure_grid(self):
        for i in range(1, 6):
            self.master.columnconfigure(index=i, weight=1)
        for i in range(0, self.available_row):
            self.master.rowconfigure(index=i, weight=1)


def on_quit():
    app.stop_current_simulation()
    root.destroy()


if __name__ == '__main__':
    freeze_support()
    root = tk.Tk()
    app = InfectionApp(root)
    root.protocol('WM_DELETE_WINDOW', on_quit)
    app.mainloop()
