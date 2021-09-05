import re

import pytest

import sisifo


UUID_REGEX = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


@pytest.fixture()
def sample_task():
    @sisifo.add_task("test")
    class SampleTask(sisifo.Task):
        def __init__(self, sample_property="default", **kwargs):
            super().__init__(**kwargs)
            self.sample_property = sample_property

    yield SampleTask

    sisifo.remove_task("test.SampleTask")


def test_task_to_dict(sample_task):
    task = sample_task()
    expected = {
        "name": "SampleTask",
        "sample_property": "default",
    }
    actual = task.to_dict()
    assert re.match(UUID_REGEX, actual["id"])
    del actual["id"]
    assert actual == expected


def test_task_from_dict_default(sample_task):
    actual = sample_task.from_dict({})
    assert type(actual) == sample_task
    assert actual.sample_property == "default"
    assert re.match(UUID_REGEX, actual.id)


def test_task_get_id_custom_value():
    task = sisifo.Task(id="task_id")
    assert task.get_id() == "task_id"


def test_task_get_name_default_value():
    task = sisifo.Task()
    assert task.get_name() == "Task"


def test_task_get_name_custom_value():
    task = sisifo.Task(name="MyTask")
    assert task.get_name() == "MyTask"


def test_task_get_set_parent():
    task = sisifo.Task()
    parent_task = sisifo.Task()
    assert task.get_parent() == None
    task.set_parent(parent_task)
    assert task.get_parent() == parent_task


def test_task_set_parent_type_error():
    task = sisifo.Task()
    with pytest.raises(TypeError):
        task.set_parent(None)


def test_task_add_child_type_error():
    task = sisifo.Task()
    with pytest.raises(TypeError):
        task.add_child(None)


def test_task_add_remove_child():
    parent = sisifo.Task()
    child = sisifo.Task()
    parent.add_child(child)
    assert parent.get_children() == [child]
    assert child.get_parent() == None
    parent.remove_child(child)
    assert parent.get_children() == []


def test_task_create_subtask():
    parent = sisifo.Task()
    child = sisifo.Task()
    parent.create_subtask(child)
    assert parent.get_children() == [child]
    assert child.get_parent() == parent


def test_task_create_subtask_type_error():
    task = sisifo.Task()
    with pytest.raises(TypeError):
        task.create_subtask("?")


@pytest.fixture()
def ensure_entity_is_empty_list_task():
    class EnsureEntityIsEmptyList(sisifo.TaskDecorator):
        def run(self, data):
            if self.task.entity_in not in data:
                data[self.task.entity_in] = []
            self.task.run(data)

    return EnsureEntityIsEmptyList


@pytest.fixture()
def append_to_entity_task():
    class AppendToEntity(sisifo.EntityTask):
        def __init__(self, value, **kwargs):
            super().__init__(**kwargs)
            self.value = value

        def run_entity(self, entity):
            return entity + [self.value]

    return AppendToEntity


def test_append_without_task_decorator(data_collection, append_to_entity_task):
    task = append_to_entity_task(value="value", entity="I do not exists")
    with pytest.raises(KeyError):
        task.run(data_collection)


def test_append_with_task_decorator(data_collection, append_to_entity_task,
                                    ensure_entity_is_empty_list_task):
    task = append_to_entity_task(value="value", entity="I do not exist")
    task = ensure_entity_is_empty_list_task(task)
    task.run(data_collection)
    task.run(data_collection)
    assert data_collection["I do not exist"] == ["value", "value"]


def test_task_decorator_wraps_task(mocker):
    mock_task = mocker.Mock(name="Task")
    mock_task.return_value = "hey"
    decorator = sisifo.TaskDecorator(mock_task)

    assert decorator.to_dict() == mock_task.to_dict()
    assert decorator.get_id() == mock_task.get_id()
    assert decorator.get_name() == mock_task.get_name()
    assert decorator.run(None) == mock_task.run(None)
    assert decorator.set_parent(None) == mock_task.set_parent(None)
    assert decorator.get_parent() == mock_task.get_parent()
    assert decorator.add_child(None) == mock_task.add_child(None)
    assert decorator.get_children() == mock_task.get_children()
    assert decorator.remove_child(None) == mock_task.remove_child(None)


def test_entity_task_entity_in_error():
    with pytest.raises(ValueError):
        sisifo.EntityTask(entity_out="out")


def test_entity_task_entity_out_default_in():
    task = sisifo.EntityTask(entity_in="in")
    assert task.entity_out == "in"


def test_entity_task_run_entity(data_collection):
    task = sisifo.EntityTask(entity_in="in", entity_out="out")
    data_collection["in"] = "entity_value"
    task.run(data_collection)
    assert data_collection["out"] == "entity_value"


def test_entity_column_task_column_in_error():
    with pytest.raises(ValueError):
        sisifo.EntityColumnTask(entity="entity")


def test_entity_column_task_column_out_default_in():
    task = sisifo.EntityColumnTask(entity="entity", column_in="in")
    assert task.column_out == "in"
