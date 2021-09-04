from concurrent.futures import ThreadPoolExecutor

import sisifo


@sisifo.add_task("common")
class ParallelPipeline(sisifo.Task):
    def __init__(self, steps=[], max_workers=None, **kwargs):
        super().__init__(**kwargs)
        self.max_workers = max_workers

        for i in steps:
            self.create_subtask(i)

    def run(self, data):
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            for task in self.get_children():
                ex.submit(task.run, data)
