from cleo import Command, argument, option


class NewCommand(Command):
    name = "new"
    description = "Creates a new Python project at <path>."

    arguments = [argument("path", "The path to create the project at.")]
    options = [
        option("name", None, "Set the resulting package name.", flag=False),
        option("src", None, "Use the src layout for the project."),
        option("py", None, "Set the Python interpreter version.")
    ]

    def handle(self):
        if self.option('py'):
            pass
        else:
            pass
