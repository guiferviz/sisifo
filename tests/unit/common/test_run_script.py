import sys

from sisifo.plugins import common as common_tasks

import pytest


def test_error_without_script():
    with pytest.raises(ValueError):
        common_tasks.RunScript()


def test_run(mocker):
    subprocess = mocker.patch("sisifo.plugins.common.run_script.subprocess")

    script = "echo 'hola'"
    task = common_tasks.RunScript(script)
    task.run(None)

    subprocess.check_call.assert_called_once_with(script, shell=True,
                                                  stdout=sys.stdout,
                                                  stderr=sys.stderr,
                                                  executable="/bin/bash")
