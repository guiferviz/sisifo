import sisifo


@sisifo.add_task("common")
class Pipeline(sisifo.Task):
    def __init__(self, steps=[], **kwargs):
        super().__init__(**kwargs)

        for i in steps:
            self.create_subtask(i)

    def run(self, data):
        for task in self.get_children():
            task.run(data)
