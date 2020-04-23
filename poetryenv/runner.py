import re
import delegator
from typing import List

from poetryenv.environments import PYENV_INSTALLED, POETRY_INSTALLED
from poetryenv.exceptions import RunnerError
from poetryenv.decorators import runner


class Runner:
    def _run(self, *args: str) -> delegator.Command:
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

    def _gen_available_versions(self) -> str:
        c = self._run(self.cmd, 'install', '-l')
        for name in c.out.splitlines():
            m = self.available_version_pattern.match(name.strip())
            if m:
                yield m.group()

    @property
    def available_versions(self) -> List[str]:
        return list(self._gen_available_versions()) if PYENV_INSTALLED else []

    def _gen_installed_available_versions(self) -> str:
        c = self._run(self.cmd, 'versions')
        for name in c.out.splitlines():
            m = self.installed_available_version_pattern.search(name)
            if m:
                yield m.group().strip()

    @property
    def installed_available_versions(self) -> List[str]:
        return list(self._gen_installed_available_versions()) if PYENV_INSTALLED else []

    def _is_available_version(self, version: str) -> bool:
        return version in self.available_versions

    def _is_installed_version(self, version: str) -> bool:
        return version in self.installed_available_versions

    @runner(cmd=cmd, is_available=PYENV_INSTALLED)
    def install(self, version: str) -> delegator.Command:
        if not self._is_available_version(version):
            raise RunnerError(
                f'Invalid version: {version}. Please check available versions using "poetryenv list"')

        c = self._run(self.cmd, 'install', '-s', version)

        return c

    @runner(cmd=cmd, is_available=PYENV_INSTALLED)
    def local(self, version: str) -> delegator.Command:
        if not self._is_installed_version(version):
            raise RunnerError(
                f'Invalid version: {version} ' +
                'Please check installed versions using "poetryenv list --installed/-i"')

        c = self._run(self.cmd, 'local', version)

        return c

    @runner(cmd=cmd, is_available=PYENV_INSTALLED)
    def current_version(self) -> delegator.Command:
        c = self._run(self.cmd, 'version-name')
        return c


class PoetryRunner(Runner):

    cmd = 'poetry'

    @runner(cmd=cmd, is_available=POETRY_INSTALLED)
    def new(self, path: str, name: str or None, src: bool) -> delegator.Command:
        name_opt = f'--name {name}' if name else ''
        src_opt = '--src' if src else ''
        c = self._run(self.cmd, 'new', name_opt, src_opt, path)
        return c
