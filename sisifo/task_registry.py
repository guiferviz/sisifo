from sisifo.abstract_task import AbstractTask
from sisifo.named_collection import AllowUpdateDecorator
from sisifo.named_collection import NamedCollectionBuilder


class TaskRegistry:
    def __init__(self):
        self._collection = (
            NamedCollectionBuilder()
            .subclass_of(AbstractTask)
            .suggestions()
            .fail_if_exists()
            .fail_if_name_none()
            .build()
        )

    def add_task(self, canonical_name: str, task: AbstractTask):
        self._collection[canonical_name] = task

    def replace_task(self, canonical_name: str, task: AbstractTask):
        allow_update = AllowUpdateDecorator(self._collection)
        allow_update[canonical_name] = task

    def get_task(self, canonical_name: str):
        return self._collection[canonical_name]

    def remove_task(self, canonical_name: str):
        del self._collection[canonical_name]

    def __contains__(self, canonical_name: str):
        return canonical_name in self._collection


_TASK_REGISTRY = TaskRegistry()


def get_task_registry() -> TaskRegistry:
    return _TASK_REGISTRY


def set_task_registry(registry: TaskRegistry) -> None:
    global _TASK_REGISTRY
    _TASK_REGISTRY = registry


def _create_canonical_name(namespace: str, task_name: str) -> str:
    return f"{namespace}.{task_name}"


def _create_canonical_name_from_class(namespace: str, task_class: type) -> str:
    task_name = task_class.__name__
    if namespace:
        return _create_canonical_name(namespace, task_name)
    return task_name


def add_task(namespace: str = ""):
    def wrapper(task_class):
        task_canonical_name = _create_canonical_name_from_class(namespace, task_class)
        get_task_registry().add_task(task_canonical_name, task_class)
        return task_class
    return wrapper


def replace_task(namespace: str = ""):
    def wrapper(task_class):
        task_canonical_name = _create_canonical_name_from_class(namespace, task_class)
        get_task_registry().replace_task(task_canonical_name, task_class)
        return task_class
    return wrapper


def get_task(canonical_name: str) -> type:
    return get_task_registry().get_task(canonical_name)


def remove_task(canonical_name: str) -> None:
    get_task_registry().remove_task(canonical_name)


def has_task(canonical_name: str) -> bool:
    return canonical_name in get_task_registry()
