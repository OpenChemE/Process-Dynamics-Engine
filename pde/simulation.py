import control
import numpy as np
from collections import OrderedDict
from copy import deepcopy
from pde.model import Model

class Simulation:

    # Initialize with simulation of 10 units time
    MIN_TIME = 10
    # Maximum possible simulation time
    MAX_TIME = 1000

    def __init__(self, model, uid):
        self.model = model
        self.id = uid
        self.reset()

    def reset(self):
        self.simulation = None
        self.active = False
        self.time = np.linspace(
            0, Simulation.MIN_TIME - 1, Simulation.MIN_TIME)
        self.inputs = np.zeros((self.model.system.inputs, Simulation.MIN_TIME))
        print('Simulation #{} created. Call activate() to activate'.format(self.id))

    def activate(self):
        if not self.active:
            self.active = True
            self.simulation = self.step_generator()
            self.simulation.send(None)
            print('Simulation #{} activated. Ready to simulate'.format(self.id))
        else:
            print(
                'Simulation #{} already active. Call reset() to deactivate'.format(self.id))

    def updateTag(self, inputs):
        if not isinstance(inputs, dict):
            raise TypeError("Input must be a dictionary of tags to update")
        for key in inputs:
            try:
                self.model.inputs[key].value = inputs[key]
                print('Updated {0} to: {1}'.format(key, inputs[key]))
            except KeyError:
                print('Tag not found in inputs: {}'.format(key))

    def step(self):
        if not self.active:
            raise ValueError("Simulation needs to be initialized first")
        assert not self.simulation is None
        try:
            T, Y = next(self.simulation)
            last_Y = Y[:, -1]
            keys = list(self.model.outputs.keys())
            for idx, y in enumerate(last_Y):
                self.model.outputs[keys[idx]] = y
            return deepcopy(self.model.outputs)
        except StopIteration:
            print('Error: Simulation not active or exceeded maximum simulation time.')

    def step_generator(self):
        while (self.active) and (self.time[-1] <= Simulation.MAX_TIME):
            inputs = [i.value for i in self.model.inputs.values()]
            self.inputs = np.column_stack((self.inputs, inputs))
            self.time = np.append(self.time, self.time[-1] + 1)
            T, Y, _ = control.forced_response(
                self.model.system, self.time, self.inputs)
            yield (T, Y)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        if not isinstance(model, Model):
            raise TypeError("Simulation model must be of type Model")
        self._model = model

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not value:
            raise ValueError("Simulation ID cannot be empty")
        self._id = value
