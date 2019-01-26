from pde import Model, Simulation, Tag

def create(system, name, inputs, outputs):
    model = Model(system, name, inputs, outputs)
    return Simulation(model, -1)

def is_active(sim):
    return sim.active

def activate(sim):
    sim.activate()

def step(sim, inputs):
    sim.update_tag(inputs)
    outputs = sim.step()
    return { tag.name: tag.value for tag in outputs.values() }
