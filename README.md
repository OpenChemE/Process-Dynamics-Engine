# Background

**Project under active development**

Process Dynamics Engine (PDE) is an online, real-time simulator for process control models described by transfer functions or state space representations. PDE is implemented in Python and uses the [Python Control Systems Library](https://github.com/python-control/python-control). Users can interact with the simulation by using an API to send control actions (e.g. increasing a reflux rate or shutting off a valve) and query process variables like temperature and pressure. PDE is intended to be an educational tool in chemical engineering process control courses.

Real world processes can be organized by the hierarchy of process controls as shown in the pyramid below. The plant is at the base layer, followed by the measurements layer with sensors and transmitters and a controls layer using consoles or panels with either manual operator control or automated loops.

![https://upload.wikimedia.org/wikipedia/commons/1/10/Functional_levels_of_a_Distributed_Control_System.svg](https://upload.wikimedia.org/wikipedia/commons/1/10/Functional_levels_of_a_Distributed_Control_System.svg)
*Source: https://en.wikipedia.org/wiki/Process_control*

**TODO: update diagram**

The design of PDE mimics real world processes with an Engine component that runs the simulation (Plant) and a Graphics component (Panel) for visualizing and manipulating process variables. Users can also interact with the simulation through the Graphics component or directly with the Engine's API.

PDE design notes:
1. Supports concurrent simulations by offloading computations to background workers
2. Supports simple SISO models or complex MIMO models
3. Graphics are decoupled from Models
4. Containerized and scalable

The development of PDE is funded by a University of British Columbia Teaching and Learning Enhancement Fund (TLEF) 2018/2019 grant.

# Usage
**Project under active development, please wait for stable version.**

1. Clone repository

```
git clone https://github.com/OpenChemE/Process-Dynamics-Engine.git
```

2. Install package

```python
pip install .
```

3. Navigate to the repository in your folder and try importing the Wood-Berry distillation model (See the Toy Model notebook)

```python
import pde
from models.distillation_models import WoodBerry
```

4. Create a simulation from the model
```python
distillation = pde.Simulation(WoodBerry(), uid='0')
distillation.activate()
```

5. Step through the simulation
```
distillation.step()
```