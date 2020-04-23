from cleo import Application
from poetryenv.new import NewCommand
from poetryenv.list import ListCommand
from poetryenv.version import VersionCommand

from poetryenv import __version__


APPLICATION_NAME = 'poetryenv'

application = Application(APPLICATION_NAME, __version__)
application.add(NewCommand())
application.add(ListCommand())
application.add(VersionCommand())
