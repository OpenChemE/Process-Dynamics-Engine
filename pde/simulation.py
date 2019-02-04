import control
import numpy as np
from copy import deepcopy
from pde.model import Model


class Simulation:

    MIN_TIME = 10
    MAX_TIME = 1000


    def __init__(self, model, sim_id):
        self.model = model
        self.sim_id = sim_id
        self.reset()


    def reset(self):
        self.active = False
        self.time = np.linspace(
                0, Simulation.MIN_TIME - 1, Simulation.MIN_TIME)
        self.inputs = np.zeros((len(self.model.inputs), Simulation.MIN_TIME))
        print(f'Simulation {self.sim_id} of {self.model.name} created. ' +
                'Call `activate()` to activate.')


    def activate(self):
        if self.active:
            print(f'Simulation {self.sim_id} already active. ' +
                    'Call `reset()` to deactivate.')
        else:
            self.active = True
            print(f'Simulation {self.sim_id} activated. '+
                    'Call `step()` to run the simulation.')


    def update_tag(self, inputs):
        if not isinstance(inputs, dict):
            raise TypeError('Input must be a dictionary of tags to update.')
        for key in inputs:
            try:
                self.model.inputs[key].value = inputs[key]
                print(f'Updated tag {key} to: {inputs[key]}.')
            except KeyError:
                print(f'Tag {key} not found in inputs.')


    # TODO: Decide how to handle first few data points in MIN_TIME
    def step(self):
        if not self.active:
            raise ValueError(f'Simulation {self.sim_id} must be activated.')
        if self.time[-1] > Simulation.MAX_TIME:
            raise ValueError(f'Simulation {self.sim_id} ' +
                    'exceeded the maximum simulation time.')

        # Get new outputs from the simulation step
        self.time = np.append(self.time, self.time[-1] + 1)
        self.inputs = np.column_stack((self.inputs,
            [tag.value for tag in self.model.inputs.values()]))
        T, yout, xout = control.forced_response(
                self.model.system, self.time, self.inputs)

        # We only use the last (newest) value in yout to update our output
        # TODO: Switch to state space for iterative calculations
        keys = list(self.model.outputs.keys())
        for i, y in enumerate(yout[:, -1]):
            self.model.outputs[keys[i]].value = y
        return deepcopy(self.model.outputs)
