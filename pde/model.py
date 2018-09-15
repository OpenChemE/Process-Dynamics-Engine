import control
from collections import OrderedDict

class Model:

    def __init__(self, system, name, inputs, outputs):
        self.system = system
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def __repr__(self):
        return 'System: \n {}'.format(self.system)

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system):
        if not isinstance(system, (control.xferfcn.TransferFunction, control.statesp.StateSpace)):
            raise ValueError(
                "System must be either Transfer Function or State Space")
        self._system = system

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Model name cannot be empty")
        self._name = name

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        if not isinstance(value, dict):
            raise TypeError("Inputs must be an ordered dictionary")
        elif not all(tag.IOtype is "INPUT" for tag in value.values()):
            raise ValueError(
                "All tags in input array must have an IOtype of 'INPUT'")
        elif not len(value) is self.system.inputs:
            raise ValueError(
                "System must have exactly {} input tags".format(self.system.inputs))
        self._inputs = OrderedDict(value)

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, value):
        if not isinstance(value, dict):
            raise ValueError("Outputs must be an ordered dictionary")
        elif not all(tag.IOtype is "OUTPUT" for tag in value.values()):
            raise ValueError(
                "All tags in output array must have an IOtype of 'OUTPUT'")
        elif not len(value) is self.system.outputs:
            raise ValueError(
                "System must have exactly {} output tags".format(self.system.outputs))
        self._outputs = OrderedDict(value)
