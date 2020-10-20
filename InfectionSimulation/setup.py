from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('gui.py', base=base, targetName = 'InfectionSimulation')
]

setup(name='Infection Simulation',
      version = '1.0',
      description = 'Simulation of how infection spreads in a population',
      options = {'build_exe': build_options},
      executables = executables)
