from pde import Model, Simulation, Tag


def create(name, system, inputs, outputs, model_id, sim_id):
    model = Model(name, system, inputs, outputs, model_id)
    return Simulation(model, sim_id)

def is_active(sim):
    return sim.active

def activate(sim):
    sim.activate()

def step(sim, inputs):
    sim.update_tag(inputs)
    outputs = sim.step()
    return { tag.name: tag.value for tag in outputs.values() }
