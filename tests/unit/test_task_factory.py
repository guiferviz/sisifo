import sisifo
from sisifo.task_factory import TaskFactory

import pytest


@pytest.fixture()
def test_task(mocker):
    mocker.patch("sisifo.task_registry._TASK_REGISTRY", sisifo.TaskRegistry())

    @sisifo.add_task("test")
    class TestTask(sisifo.Task):
        pass

    return TestTask


def test_create_task(test_task):
    task = sisifo.create_task({
        "task": "test.TestTask",
    })
    assert type(task) == test_task


def test_get_task_class_from_config():
    with pytest.raises(ValueError):
        TaskFactory().get_task_class_from_config(dict(name="something"))
