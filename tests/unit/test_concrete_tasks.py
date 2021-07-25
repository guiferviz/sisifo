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


def test_to_config_task(sample_task):
    task = sample_task()
    expected = {
        "name": "SampleTask",
        "sample_property": "default",
    }
    actual = task.to_config()

    assert re.match(UUID_REGEX, actual["id"])
    del actual["id"]
    assert actual == expected


def test_from_config_default(sample_task):
    actual = sample_task.from_config({})

    assert type(actual) == sample_task
    assert actual.sample_property == "default"
    assert re.match(UUID_REGEX, actual.id)


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
