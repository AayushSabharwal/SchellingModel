#Infection Simulation using Agent Based Modeling

This project aims to simulate the spread of an infection in a population
 using Agent Based modeling through the [mesa library for Python](https://github.com/projectmesa/mesa/).
 Individuals are represented by agents on a grid. Initially, a fraction
 of them are infected, and each iteration (hour) they have a chance to infect
 nearby agents. The simulation is a [Compartmental Epidemiology Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology),
 specifically a configurable SIRS model, which can be tweaked into an SI or
 SIR model, and can also simulate vaccination, population growth and
 death. For more insight into how the simulation works, it is recommended
 to view the code, and click on the parameter names in the GUI for a
 description.
    
The easiest way to run this simulation is to get the latest executable
 release. To run the code, mesa and scipy should be installed in your Python
 environment. The gui.py file is the sole entry point to the simulation. The
 simulation can be viewed as a live updating plot through Dynamic Run, or
 for larger scale/longer simulations, the data can be logged as a csv
 using Static Run. 