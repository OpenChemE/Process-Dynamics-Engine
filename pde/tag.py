class Tag:

    def __init__(self, name, desc, IOtype, value=0):
        self.name = name
        self.desc = desc
        self.IOtype = IOtype
        self.value = value

    def __repr__(self):
        return '{2} Tag: {0} ({1}). Value: {3}'.format(self.name, self.desc, self.IOtype, self.value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Tag name cannot be empty")
        self._name = value

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        if not value:
            raise ValueError("Tag description cannot be empty")
        self._desc = value

    @property
    def IOtype(self):
        return self._IOtype

    @IOtype.setter
    def IOtype(self, value):
        if not value in ['INPUT', 'OUTPUT']:
            raise ValueError("IO Type must be either 'INPUT' or 'OUTPUT'")
        self._IOtype = value
