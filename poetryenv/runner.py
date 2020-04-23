import re
import delegator

from poetryenv.environments import PYENV_INSTALLED, POETRY_INSTALLED
from poetryenv.exceptions import RunnerError
from poetryenv.decorators import runner


class Runner:
    def run(self, *args: str) -> delegator.Command:
        line = ' '.join(args)
        c = delegator.run(line)
        c.block()
        if c.return_code != 0:
            raise RunnerError(f'Failed to run command: {line}')
        return c


class PyenvRunner(Runner):

    cmd = 'pyenv'
    available_version_pattern = re.compile(r'\d\.\d(.\d+|-dev)')
    installed_available_version_pattern = re.compile(r' \d\.\d(.\d+|-dev)')

    def __init__(self):
        self.available_versions = [] if not PYENV_INSTALLED else list(
            self._gen_available_versions())
        self.installed_available_versions = [] if not PYENV_INSTALLED else list(
            self._gen_installed_available_versions())

    def _gen_available_versions(self) -> str:
        c = self.run(self.cmd, 'install', '-l')
        for name in c.out.splitlines():
            m = self.available_version_pattern.match(name.strip())
            if m:
                yield m.group()

    def _gen_installed_available_versions(self) -> str:
        c = self.run(self.cmd, 'versions')
        for name in c.out.splitlines():
            m = self.installed_available_version_pattern.search(name)
            if m:
                yield m.group().strip()

    def _is_available_version(self, version: str) -> bool:
        return version in self.available_versions

    def _is_installed_version(self, version: str) -> bool:
        return version in self.installed_available_versions

    @runner(cmd=cmd, is_available=PYENV_INSTALLED)
    def install(self, version: str) -> delegator.Command:
        if not self._is_available_version(version):
            raise RunnerError(
                f'Invalid version: {version}. Please check available versions using "poetryenv list"')

        try:
            c = self.run(self.cmd, 'install', '-s', version)
        except RunnerError as err:
            raise RunnerError(err)

        return c

    @runner(cmd=cmd, is_available=PYENV_INSTALLED)
    def local(self, version: str) -> delegator.Command:
        if not self._is_installed_version(version):
            raise RunnerError(
                f'Invalid version: {version}.' +
                'Please check installed versions using "poetryenv list --installed/-i"')

        try:
            c = self.run(self.cmd, 'local', version)
        except RunnerError as err:
            raise RunnerError(err)

        return c

    @runner(cmd=cmd, is_available=PYENV_INSTALLED)
    def current_version(self) -> delegator.Command:
        try:
            c = self.run(self.cmd, 'version-name')
        except RunnerError as err:
            raise RunnerError(err)
        return c


class PoetryRunner(Runner):

    cmd = 'poetry'

    @runner(cmd=cmd, is_available=POETRY_INSTALLED)
    def new(self, path: str, name: str or None, src: bool) -> delegator.Command:
        name_opt = f'--name {name}' if name else ''
        src_opt = '--src' if src else ''
        c = self.run(self.cmd, 'new', name_opt, src_opt, path)
        return c
