from cleo import Command, option

from poetryenv import pyenv_runner


class ListCommand(Command):
    name = "list"
    description = "Display available Python versions"

    options = [option('installed', 'i', 'Installed Python versions')]

    def handle(self):
        if self.option('installed'):
            lines = ('Installed Python versions:\n' +
                     '\n'.join(pyenv_runner.installed_available_versions))
        else:
            lines = 'Available Python versions:\n' + '\n'.join(pyenv_runner.available_versions)
        self.line(lines)
