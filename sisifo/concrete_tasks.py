import uuid

from sisifo.abstract_task import AbstractTask
from sisifo.task_factory import TaskFactory
from sisifo import utils


class Task(AbstractTask):
    @classmethod
    def from_dict(cls, config_dict):
        return cls(**config_dict)

    def __init__(self, id=None, name=None, factory=None):
        self.id = id or str(uuid.uuid4())
        self.name = name or self.__class__.__name__
        self._factory = factory or TaskFactory()
        self._parent = None
        self._children = []

    def to_dict(self):
        properties = vars(self)
        public_properties = {
            k: v for k, v in properties.items() if not k.startswith("_")
        }
        return public_properties

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def run(self, _):
        pass

    def set_parent(self, parent: AbstractTask):
        if not isinstance(parent, AbstractTask):
            raise TypeError("`parent` should be instance of AbstractTask")
        self._parent = parent

    def get_parent(self):
        return self._parent

    def add_child(self, parent: AbstractTask) -> None:
        if not isinstance(parent, AbstractTask):
            raise TypeError("`task` should be instance of AbstractTask")
        self._children.append(parent)

    def get_children(self) -> list:
        return self._children

    def remove_child(self, child) -> None:
        self._children.remove(child)

    def create_subtask(self, task_or_dict):
        task = task_or_dict
        if not isinstance(task_or_dict, AbstractTask):
            if type(task_or_dict) == dict:
                task = self._factory.create_task(task_or_dict)
            else:
                raise TypeError(f"Cannot infer task from type: {type(task_or_dict)}")
        self.add_child(task)
        task.set_parent(self)
        return task


class TaskDecorator(AbstractTask):
    @classmethod
    def from_dict(cls, _):
        raise NotImplementedError()

    def __init__(self, task):
        self.task = task

    def to_dict(self):
        return self.task.to_dict()

    def get_id(self):
        return self.task.get_id()

    def get_name(self):
        return self.task.get_name()

    def run(self, data):
        return self.task.run(data)

    def set_parent(self, parent):
        return self.task.set_parent(parent)

    def get_parent(self):
        return self.task.get_parent()

    def add_child(self, child):
        return self.task.add_child(child)

    def get_children(self):
        return self.task.get_children()

    def remove_child(self, child):
        return self.task.remove_child(child)


class EntityTask(Task):
    def __init__(self, entity=None, entity_in=None, entity_out=None, **kwargs):
        super().__init__(**kwargs)
        self.entity_in, self.entity_out = utils.validate_entity_in_out(
                entity, entity_in, entity_out)

    def run(self, data):
        df = data[self.entity_in]
        data[self.entity_out] = self.run_entity(df)

    def run_entity(self, df):
        return df


class EntityColumnTask(EntityTask):
    def __init__(self, column=None, column_in=None, column_out=None, **kwargs):
        super().__init__(**kwargs)
        self.column_in, self.column_out = utils.validate_column_in_out(
            column, column_in, column_out)
