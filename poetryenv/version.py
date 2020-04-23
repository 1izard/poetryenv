import traceback
import sys
from cleo import Command

from poetryenv import pyenv_runner
from poetryenv.exceptions import RunnerError


class VersionCommand(Command):
    name = 'version'
    description = 'Show current Python version'

    def handle(self):
        try:
            c = pyenv_runner.current_version()
            self.line(c.out)
        except RunnerError:
            traceback.print_exc(file=sys.stderr)
