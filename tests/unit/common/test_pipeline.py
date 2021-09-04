import sisifo
from sisifo.plugins import common as common_tasks

import pytest


@pytest.fixture()
def sample_task():
    @sisifo.add_task("test")
    class SampleTask(sisifo.Task):
        pass

    yield SampleTask

    sisifo.remove_task("test.SampleTask")


def test_empty_pipeline_constructor():
    common_tasks.Pipeline()


def test_pipeline_constructor_mixed_tasks(sample_task):
    pipeline = common_tasks.Pipeline(steps=[
        {"task": "test.SampleTask"},
        sample_task(),
    ])
    assert len(pipeline.get_children()) == 2
    assert all(type(i) == sample_task for i in pipeline.get_children())


def test_add_tasks_after_creation(sample_task):
    pipeline = common_tasks.Pipeline()
    assert len(pipeline.get_children()) == 0
    pipeline.create_subtask(sample_task())
    assert len(pipeline.get_children()) == 1
    pipeline.create_subtask({"task": "test.SampleTask"})
    assert len(pipeline.get_children()) == 2


def test_run(data_collection):
    class SampleTask1(sisifo.Task):
        def run(self, data):
            data["sample_list"] = [1]

    class SampleTask2(sisifo.Task):
        def run(self, data):
            data["sample_list"].append(2)

    pipeline = common_tasks.Pipeline(steps=[
        SampleTask1(),
        SampleTask2(),
    ])
    pipeline.run(data_collection)

    assert "sample_list" in data_collection
    assert data_collection["sample_list"] == [1, 2]
