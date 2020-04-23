import traceback
import sys
from cleo import Command, argument

from poetryenv import pyenv_runner
from poetryenv.exceptions import RunnerError


class LocalCommand(Command):
    name = 'local'
    description = 'Set or show the local application-specific Python version'

    version = argument('version', 'Python version to set', optional=True)

    def handle(self):
        if self.version:
            try:
                c = pyenv_runner.local(self.version)
                self.line(c.out)
            except RunnerError:
                traceback.print_exc(file=sys.stderr)
        else:
            try:
                c = pyenv_runner.current_version()
                self.line(c.out)
            except RunnerError:
                traceback.print_exc(file=sys.stderr)
