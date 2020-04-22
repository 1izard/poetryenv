from cleo import Command

from poetryenv import pyenv_runner


class ListCommand(Command):
    name = "list"
    description = "Display available python versions"

    def handle(self):
        lines = 'Available Python versions:\n' + '\n'.join(pyenv_runner.available_versions)
        self.line(lines)
        return
