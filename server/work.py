from pde import Model, Simulation, Tag

def create_simulation(system, name, inputs, outputs):
    model = Model(system, name, inputs, outputs)
    return Simulation(model, -1)
