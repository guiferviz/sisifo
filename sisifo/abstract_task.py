import abc


class Executable(abc.ABC):
    @abc.abstractmethod
    def run(self, data):
        pass


class Serializable(abc.ABC):
    @classmethod
    @abc.abstractclassmethod
    def from_dict(cls, factory, config):
        pass

    @abc.abstractmethod
    def to_dict(self):
        pass


class Nesteable(abc.ABC):
    @abc.abstractmethod
    def set_parent(self, parent):
        pass

    @abc.abstractmethod
    def get_parent(self):
        pass

    @abc.abstractmethod
    def add_child(self, child):
        pass

    @abc.abstractmethod
    def get_children(self):
        pass

    @abc.abstractmethod
    def remove_child(self, child):
        pass


class AbstractTask(Executable, Serializable, Nesteable):
    @abc.abstractmethod
    def get_id(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass
