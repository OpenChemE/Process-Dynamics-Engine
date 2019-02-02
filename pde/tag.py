from enum import Enum


class TagType(Enum):

    INPUT = 0
    OUTPUT = 1


class Tag:

    def __init__(self, tag_id, name, description, tag_type, value=0):
        self.tag_id = tag_id
        self.name = name
        self.description = description
        self.tag_type = tag_type
        self.value = value

    def __repr__(self):
        return f'{self.tag_type} Tag #{self.tag_id}: {self.name} ' + \
                f'({self.description}). Value: {self.value}'
