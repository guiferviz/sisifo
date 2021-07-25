import subprocess
import sys

import sisifo


@sisifo.add_task("common")
class RunScript(sisifo.Task):
    def __init__(self, script=None, executable="/bin/bash", **kwargs):
        super().__init__(**kwargs)

        if not script:
            raise ValueError("An script should be provided")

        self.script = script
        self.executable = executable

    def run(self, _):
        subprocess.check_call(self.script, shell=True,
                              stdout=sys.stdout, stderr=sys.stderr,
                              executable=self.executable)
