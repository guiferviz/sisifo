from sisifo.task_registry import get_task_registry


class TaskFactory:
    def get_task_class_from_name(self, task_name):
        return get_task_registry().get_task(task_name)

    def get_task_class_from_config(self, task_config):
        task_name = task_config.pop("task", None)
        if task_name is None:
            raise ValueError("Task name should be provided")
        task_class = self.get_task_class_from_name(task_name)
        return task_class

    def create_task_from_class(self, task_class, task_factory, task_config):
        task_config["factory"] = task_factory
        return task_class.from_config(task_config)

    def create_task_from_config(self, task_factory, task_config):
        task_class = self.get_task_class_from_config(task_config)
        task = self.create_task_from_class(task_class, task_factory, task_config)
        return task

    def create_task(self, task_config: dict):
        # TODO: apply plugins to `self` TaskFactory
        task_factory = self
        return self.create_task_from_config(task_factory, task_config)


def create_task(task_config: dict):
    return TaskFactory().create_task(task_config)
