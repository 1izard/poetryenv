import os
import re
import delegator

from poetryenv.exceptions import RunnerError


class Runner:
    def __init__(self, cmd: str):
        self.cmd = cmd

    def run(self, *args: str) -> delegator.Command:
        line = ' '.join((self.cmd, ) + args)
        c = delegator.run(line)
        c.block()
        if c.return_code != 0:
            raise RunnerError(f'Failed to run command: {line}')
        return c


class PyenvRunner(Runner):

    available_version_pattern = re.compile(r'\d\.\d(.\d+|-dev)')
    installed_available_version_pattern = re.compile(r' \d\.\d(.\d+|-dev) ')

    def __init__(self):
        super().__init__('pyenv')
        self.is_installed = bool(os.environ.get('PYENV_SHELL') or os.environ.get('PYENV_ROOT'))
        self.available_versions = [] if not self.is_installed else list(
            self._gen_available_versions())
        self.installed_available_versions = [] if not self.is_installed else list(
            self._gen_installed_available_versions())

    def _gen_available_versions(self) -> str:
        c = super().run('install', '-l')
        for name in c.out.splitlines():
            m = self.available_version_pattern.match(name.strip())
            if m:
                yield m.group()

    def _gen_installed_available_versions(self) -> str:
        c = super().run('versions')
        for name in c.out.splitlines():
            m = self.installed_available_version_pattern.match(name.strip())
            if m:
                yield m.group()

    def _is_available_version(self, version: str) -> bool:
        return version in self.available_versions

    def _is_installed_version(self, version: str) -> bool:
        return version in self.installed_available_versions

    def install(self, version: str) -> delegator.Command:
        if not self.is_installed:
            raise RunnerError(
                f'Failed to install python {version}; Pyenv is not installed. Please install Pyenv.')

        if not self._is_available_version(version):
            raise RunnerError(
                f'Invalid version: {version}. Please see available versions to exec "poetryenv new --list"')

        try:
            c = super().run('install', '-s', version)
        except RunnerError as err:
            raise RunnerError(err)

        return c


class PoetryRunner(Runner):

    def __init__(self):
        super().__init__('poetry')

    def new(self, path: str, name: str or None, src: bool) -> delegator.Command:
        name_opt = f'--name {name}' if name else ''
        src_opt = '--src' if src else ''
        c = super().run(name_opt, src_opt, path)
        return c
