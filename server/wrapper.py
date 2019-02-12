from pde import Model, Simulation, Tag


def create(model_id, sim_id, name, system, inputs, outputs):
    model = Model(model_id, name, system, inputs, outputs)
    return Simulation(sim_id, model)

def is_active(sim):
    return sim.active

def activate(sim):
    sim.activate()

def step(sim, inputs):
    sim.update_tag(inputs)
    outputs = sim.step()
    return { tag.name: tag.value for tag in outputs.values() }
