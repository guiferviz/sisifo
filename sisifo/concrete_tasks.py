import uuid

from sisifo.abstract_task import AbstractTask
from sisifo.task_factory import TaskFactory
from sisifo.utils import params


class Task(AbstractTask):
    @classmethod
    def from_config(cls, config):
        return cls(**config)

    def __init__(self, id=None, name=None, factory=None):
        self.id = id or str(uuid.uuid4())
        self.name = name or self.__class__.__name__
        self._factory = factory or TaskFactory()
        self._parent = None
        self._children = []

    def to_config(self):
        properties = vars(self)
        public_properties = {
            k: v for k, v in properties.items() if not k.startswith("_")
        }
        return public_properties

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def run(self, data):
        return data

    def set_parent(self, parent: AbstractTask):
        if not isinstance(parent, AbstractTask):
            raise ValueError("`parent` should be instance of AbstractTask")
        self._parent = parent

    def get_parent(self):
        return self._parent

    def add_child(self, task) -> None:
        if not isinstance(task, AbstractTask):
            raise ValueError("`task` should be instance of AbstractTask")
        self._children.append(task)

    def get_children(self) -> list:
        return self._children

    def remove_child(self, child) -> None:
        self._children.remove(child)

    def create_subtask(self, task_or_config):
        task = task_or_config
        if not isinstance(task_or_config, AbstractTask):
            if type(task_or_config) == dict:
                task = self._factory.create_task(task_or_config)
            else:
                raise ValueError("Cannot infer task from type: {type(task_or_config)}")
        self.add_child(task)
        task.set_parent(self)
        return task


class TaskDecorator(AbstractTask):
    @classmethod
    def from_config(cls, _):
        raise NotImplementedError()

    def __init__(self, task):
        self.task = task

    def to_config(self):
        return self.task.to_config()

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
        return self.task.remove_children(child)


class EntityTask(Task):
    def __init__(self, entity=None, entity_in=None, entity_out=None, **kwargs):
        super().__init__(**kwargs)
        self.entity_in, self.entity_out = params.validate_entity_in_out(
                entity, entity_in, entity_out)

    def run(self, data):
        df = data[self.entity_in]
        data[self.entity_out] = self.run_entity(df)

    def run_entity(self, df):
        return df


class EntityColumnTask(EntityTask):
    def __init__(self, column=None, column_in=None, column_out=None, **kwargs):
        super().__init__(**kwargs)
        self.column_in, self.column_out = params.validate_column_in_out(
            column, column_in, column_out)
