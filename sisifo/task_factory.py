from sisifo.task_registry import get_task_registry


class TaskFactory:
    def get_task_class_from_name(self, task_name):
        return get_task_registry().get_task(task_name)

    def get_task_class_from_dict(self, task_dict):
        task_name = task_dict.pop("task", None)
        if task_name is None:
            raise ValueError("Task name should be provided")
        task_class = self.get_task_class_from_name(task_name)
        return task_class

    def create_task_from_class(self, task_class, task_factory, task_dict):
        task_dict["factory"] = task_factory
        return task_class.from_dict(task_dict)

    def create_task_from_dict(self, task_factory, task_dict):
        task_class = self.get_task_class_from_dict(task_dict)
        task = self.create_task_from_class(task_class, task_factory, task_dict)
        return task

    def create_task(self, task_dict: dict):
        # TODO: apply plugins to `self` TaskFactory
        task_factory = self
        return self.create_task_from_dict(task_factory, task_dict)


def create_task(task_dict, **kwargs):
    return TaskFactory().create_task(task_dict or kwargs)
