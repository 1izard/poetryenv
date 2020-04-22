from cleo import Application
from poetryenv.new import NewCommand

from poetryenv import __version__


APPLICATION_NAME = 'poetryenv'

application = Application(APPLICATION_NAME, __version__)
application.add(NewCommand())
