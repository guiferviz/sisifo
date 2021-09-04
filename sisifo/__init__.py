"""Sísifo task runner.

Generic framework for running tasks over a data collection.
"""

from sisifo._version import __version__  # noqa
from sisifo.abstract_task import AbstractTask  # noqa
from sisifo.concrete_tasks import EntityColumnTask  # noqa
from sisifo.concrete_tasks import EntityTask  # noqa
from sisifo.concrete_tasks import Task  # noqa
from sisifo.concrete_tasks import TaskDecorator  # noqa
from sisifo.data_collection import DataCollection  # noqa
from sisifo.task_factory import TaskFactory  # noqa
from sisifo.task_factory import create_task  # noqa
from sisifo.task_registry import TaskRegistry  # noqa
from sisifo.task_registry import add_task  # noqa
from sisifo.task_registry import get_task  # noqa
from sisifo.task_registry import get_task_registry  # noqa
from sisifo.task_registry import has_task  # noqa
from sisifo.task_registry import remove_task  # noqa
from sisifo.task_registry import replace_task  # noqa
from sisifo.task_registry import set_task_registry  # noqa
from sisifo.named_collection import NamedCollection  # noqa
from sisifo.named_collection import NamedCollectionDecorator  # noqa
from sisifo import plugins  # noqa


__author__ = "guiferviz"


def greet():
    """Print a silly sentence. """

    print("The easiest task is the one performed by someone else.\n"
          " - Sísifo Python library")
