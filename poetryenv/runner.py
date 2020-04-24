import os
import re
import toml
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
    available_version_pattern = re.compile(r'\d\.\d.\d+')
    installed_available_version_pattern = re.compile(r' \d\.\d.\d+')

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

    def is_available_version(self, version: str) -> bool:
        return version in self.available_versions

    def is_installed_version(self, version: str) -> bool:
        return version in self.installed_available_versions

    @runner(cmd=cmd, is_available=PYENV_INSTALLED)
    def install(self, version: str) -> delegator.Command:
        if not self.is_available_version(version):
            raise RunnerError(
                f'Invalid version: {version}. Please check available versions using "poetryenv list"')

        c = self._run(self.cmd, 'install', '-s', version)

        return c

    def local(self, version: str, dest_path: str):
        if not self.is_installed_version(version):
            raise RunnerError(
                f'Invalid version: {version} ' +
                'Please check installed versions using "poetryenv list --installed/-i"')

        python_version_path = os.path.join(dest_path, '.python-version')
        with open(python_version_path, 'w') as f:
            f.write(version)


class PoetryRunner(Runner):

    cmd = 'poetry'

    @runner(cmd=cmd, is_available=POETRY_INSTALLED)
    def new(self, path: str, name: str or None, src: bool) -> delegator.Command:
        name_opt = f'--name {name}' if name else ''
        src_opt = '--src' if src else ''
        c = self._run(self.cmd, 'new', name_opt, src_opt, path)
        return c

    def update_python_version(self, project_path: str, version: str):
        pyproject_path = os.path.join(project_path, 'pyproject.toml')
        with open(pyproject_path, 'r') as f:
            pyproject = toml.load(f)

        major, minor, _ = version.split('.')
        pyproject['tool']['poetry']['dependencies']['python'] = f'^{major}.{minor}'

        with open(pyproject_path, 'w') as f:
            toml.dump(pyproject, f)
