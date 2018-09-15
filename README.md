# Background

**Project under active development**

Process Dynamics Engine (PDE) is an online, real-time simulator for process control models described by transfer functions or state space representations. PDE is implemented in Python and uses the [Python Control Systems Library](https://github.com/python-control/python-control). Users can interact with the simulation by using an API to send control actions (e.g. increasing a reflux rate or shutting off a valve) and query process variables like temperature and pressure. PDE is intended to be an educational tool in chemical engineering process control courses.

Real world processes can be organized by the hierarchy of process controls as shown in the pyramid below. The plant is at the base layer, followed by the measurements layer with sensors and transmitters and a controls layer using consoles or panels with either manual operator control or automated loops.

The design of PDE mimics real world processes with an Engine component that runs the simulation (Plant) and a Graphics component (Panel) for visualizing and manipulating process variables. Users can also interact with the simulation through the Graphics component or directly with the Engine's API.

PDE design notes:
1. Supports concurrent simulations by offloading computations to background workers
2. Supports simple SISO models or complex MIMO models
3. Graphics are decoupled from Models
4. Containerized and scalable

The development of PDE is funded by a University of British Columbia Teaching and Learning Enhancement Fund (TLEF) 2018/2019 grant.
