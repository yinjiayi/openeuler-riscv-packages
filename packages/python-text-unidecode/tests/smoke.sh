#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q python-text-unidecode python3 python3-pytest
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cd "$work"
python3 - "$work" <<'PY'
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import text_unidecode

expected = {
    '.gitignore': '71b86d8c3e442c79b3db00062419bd6495dd4c25507a95f399eaea3c620ce6d1',
    '.travis.yml': '29eba1eb2b50e3fd861c38875fb127e6649821ca88686307ccce2df77b0e3320',
    'LICENSE': '3938e7535c3e4ef7e6363de9b693fe3bafe3c4a5e5f4925cd48375096fe7afd5',
    'MANIFEST.in': '1f81e00b1e507cbd4e571a76de35ffcdc8e06805936efa11a66c1ec8b284e5f2',
    'README.rst': '36c543976acf07b2da4bbfa6ba062f5a25bd7655cd7bbaf1639b33844d225251',
    '_dump.pl': '503e1e862db754ddf759fcf2c5a1cd734a2d8347f6af2287017e9d7dc52f9259',
    'setup.cfg': '9dd20a5ada090b01dd22055f32bdaa56315d3a14b0fd168dbe12013fa09fe5b1',
    'setup.py': '919680356cc24012302df432a75a00d243ddda2bd81c5bac8d74fe29b4cad9c5',
    'src/text_unidecode/__init__.py': 'fe1112aa5bc647f713cb4a2bc8fba8cab567b42388203edb1c303ecb6d88d628',
    'src/text_unidecode/data.bin': '7924666da4ce0ad24d4b8142b330e6d8e89465cd883934724cd9e4b7d8130f09',
    'test_unidecode.py': '9173a468aa0b18ffe1ed5313225225ac592e3ae959e223a04642eae962169c8b',
    'tox.ini': 'e8763d49f167671266af3b673ca81d3663c8ada8502055e46e0481570c78bc2d',
}
def owned(path):
    assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}\n', str(path)], text=True).strip() == 'python-text-unidecode'

work = Path(sys.argv[1]).resolve()
source = Path('/usr/share/python-text-unidecode/source')
assert len(expected) == 12
assert {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()} == set(expected)
for relative, digest in expected.items():
    p = source / relative
    assert not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest() == digest, relative
    owned(p)
assert sys.version_info[:2] == (3, 11)
assert importlib.metadata.version('text-unidecode') == '1.3'
module = Path(text_unidecode.__file__).resolve().parent
assert str(module).startswith(('/usr/lib/python3.11/site-packages/', '/usr/lib64/python3.11/site-packages/'))
assert not module.is_relative_to(source) and not module.is_relative_to(work)
assert {p.name for p in module.iterdir() if p.is_file()} == {'__init__.py', 'data.bin'}
for filename in ('__init__.py', 'data.bin'):
    p = module / filename
    assert not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest() == expected['src/text_unidecode/' + filename]
    owned(p)
suite = work / 'installed-suite'
suite.mkdir()
shutil.copy2(source / 'test_unidecode.py', suite / 'test_unidecode.py')
assert hashlib.sha256((suite / 'test_unidecode.py').read_bytes()).hexdigest() == expected['test_unidecode.py']
assert {p.name for p in suite.iterdir()} == {'test_unidecode.py'}
print(json.dumps({'installed_module': str(module), 'rpm_owned_original_files': 12,
                  'installed_runtime_and_data_files': 2, 'original_test_functions': 3,
                  'static_parameter_cases': 133,
                  'boundary': 'Ownership and original bytes checked; full installed default runs next, not a test-pass count.'}))
PY
# Empty tox posargs produce this exact unfiltered original pytest command.
# No copied runtime or src directory can shadow the authentic installed RPM.
cd "$work/installed-suite"
py.test
printf '%s\n' 'text-unidecode installed original complete default suite passed'
