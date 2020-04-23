import traceback
import sys
from cleo import Command, argument, option
from yaspin import yaspin

from poetryenv import pyenv_runner, poetry_runner
from poetryenv.exceptions import RunnerError


class NewCommand(Command):
    name = "new"
    description = "Creates a new Python project at <path>."

    arguments = [argument("path", "The path to create the project at.")]
    options = [
        option("name", None, "Set the resulting package name.", flag=False),
        option("src", None, "Use the src layout for the project."),
        option("py", None, "Set the Python version.", flag=False, value_required=True),
    ]

    def handle(self):
        version = self.option('py')
        with yaspin(text=f'Creating new python project') as sp:
            if version:
                try:
                    c_pye_install = pyenv_runner.install(version)
                    self.line(c_pye_install.out)
                except RunnerError:
                    traceback.print_exc(file=sys.stderr)
                    sp.fail(text='[Failed]')
                    return

                sp.write(f'> Installing python {version} is completed.')

                try:
                    pyenv_runner.local(version)
                except RunnerError:
                    traceback.print_exc(file=sys.stderr)
                    sp.fail(text='[Failed]')
                    return

                sp.write(f'> Switch Python version to {version}')

            try:
                c_poe = poetry_runner.new(
                    self.argument('path'),
                    self.option('name'),
                    self.option('src')
                )
                self.line(c_poe.out)
            except RunnerError:
                traceback.print_exc(file=sys.stderr)
                sp.fail(text='[Failed]')
                return

            sp.write('> Creating new python project is completed.')

            sp.ok("✔")
