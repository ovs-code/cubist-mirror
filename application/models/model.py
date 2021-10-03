from abc import ABC, abstractmethod

class Model(ABC):
    name = None
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def infer(self, data):
        pass

    @abstractmethod
    def destroy(self):
        pass

class EmptyModel(Model):
    def __init__(self):
        self.name = 'EMPTY'
        self.image = 'blank.jpg'
    def load(self):
        pass
    def infer(self, data):
        return dict(output = data['image'])
    def destroy(self):
        pass