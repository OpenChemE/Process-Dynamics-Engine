class Model:

    def __init__(self, name, system, inputs, outputs, model_id):
        self.name = name
        self.system = system
        self.inputs = inputs
        self.outputs = outputs
        self.model_id = model_id

    def __repr__(self):
        return f'Model #{self.model_id}: {self.name}\n{self.system}'
