class Model:

    def __init__(self, model_id, name, system, inputs, outputs):
        self.model_id = model_id
        self.name = name
        self.system = system
        self.inputs = inputs
        self.outputs = outputs

    def __repr__(self):
        return f'Model #{self.model_id}: {self.name}\n{self.system}'
