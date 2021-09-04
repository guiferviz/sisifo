from unittest.mock import call

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
    common_tasks.ParallelPipeline()


def test_pipeline_constructor_mixed_tasks(sample_task):
    pipeline = common_tasks.ParallelPipeline(steps=[
        {"task": "test.SampleTask"},
        sample_task(),
    ])
    assert len(pipeline.get_children()) == 2
    assert all(type(i) == sample_task for i in pipeline.get_children())


def test_add_tasks_after_creation(sample_task):
    pipeline = common_tasks.ParallelPipeline()
    assert len(pipeline.get_children()) == 0
    pipeline.create_subtask(sample_task())
    assert len(pipeline.get_children()) == 1
    pipeline.create_subtask({"task": "test.SampleTask"})
    assert len(pipeline.get_children()) == 2


def test_run(data_collection, mocker, sample_task):
    executor = mocker.patch("sisifo.plugins.common.parallel_pipeline.ThreadPoolExecutor")

    t1 = sample_task()
    t2 = sample_task()
    pipeline = common_tasks.ParallelPipeline([t1, t2], max_workers=2)
    pipeline.run(data_collection)

    executor.assert_called_once_with(max_workers=2)
    executor.return_value.__enter__.return_value.submit.assert_has_calls([
        call(t1.run, data_collection),
        call(t2.run, data_collection),
    ])  # Order is important.
