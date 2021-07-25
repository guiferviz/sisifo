import sisifo

import pytest


@pytest.fixture()
def test_task_no_namespace(mocker):
    mocker.patch("sisifo.task_registry._TASK_REGISTRY", sisifo.TaskRegistry())

    @sisifo.add_task()
    class TestTask(sisifo.Task):
        pass

    return TestTask


@pytest.fixture()
def test_task(mocker):
    mocker.patch("sisifo.task_registry._TASK_REGISTRY", sisifo.TaskRegistry())

    @sisifo.add_task("test")
    class TestTask(sisifo.Task):
        pass

    return TestTask


def test_has_task(test_task):
    assert sisifo.has_task("test.TestTask")


def test_has_task_no_namespace(test_task_no_namespace):
    assert sisifo.has_task("TestTask")


def test_get_task(test_task):
    assert sisifo.get_task("test.TestTask") == test_task


def test_not_has_task():
    assert not sisifo.has_task("test.TestTask")


def test_get_task_error():
    with pytest.raises(KeyError):
        sisifo.get_task("test.TestTask")


def test_add_task_error_on_existing_task(test_task):
    with pytest.raises(ValueError):
        @sisifo.add_task("test")
        class TestTask(sisifo.Task):
            pass


def test_replace(test_task):
    @sisifo.replace_task("test")
    class TestTask(sisifo.Task):
        def run(self, _):
            pass

    assert sisifo.get_task("test.TestTask") != test_task
    assert sisifo.get_task("test.TestTask") == TestTask
