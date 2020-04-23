import os


def poetry_installed():
    paths = os.environ.get('PATH', '')
    poetry_path = os.path.join('.poetry', 'bin')
    return poetry_path in paths


PYENV_INSTALLED = bool(os.environ.get('PYENV_SHELL') or os.environ.get('PYENV_ROOT'))
POETRY_INSTALLED = poetry_installed()
