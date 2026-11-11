#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q python-case-converter python3 python3-pip python3-build python3-pyproject-hooks python3-pytest python3-pytest-cov python3-coverage make python-pip-wheel python-setuptools python-wheel-wheel
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME
export PIP_NO_INDEX=1 PIP_FIND_LINKS=/usr/share/python-wheels
export PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
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
import sysconfig
import zipfile
import caseconverter

expected = {
    '.gitignore': '79b6f8054f8ef5e9e78c18174bf57caf29b11410166b9268d6923e87520eb88f',
    '.gitlab-ci.yml': '4fe76fc977df8a8819b6220916164cad11d5f7717097fe4db4973954ff4b441a',
    '.vscode/launch.json': 'ff931278a9c91340a087f896c5ef7c5cf7f2095cb16dde0a7b7aa106a1a84a0c',
    '.vscode/settings.json': 'de96f8a0e6d285ec3c7f4d12782af3f7a27fe54374605bebf60af2117a8b690e',
    'LICENSE': 'bbd598b6c4f2a5031905ae777c675f91608afc3080999d62b884b90d3bd93586',
    'Makefile': 'a82ef1a336b5a3b3071de4f4e701c97910629debdcd794ef847890a8b254ed74',
    'README.md': '5e550f6a6b3f952cb804d733dfafeb0c3b78ea93b58bfee17f044d0f243c5d82',
    'caseconverter/__init__.py': 'fa7e277f7e29de0b9ce978aa22605178cdf4453451c504fb43080cdec2a8b76c',
    'caseconverter/boundaries.py': '7cd9d6378a86e787ffb022a04096d604760e6528821520a53409d4bc63e02c0f',
    'caseconverter/camel.py': '5c42cdbbb9d36db2bffa6646a92fee909609a9a73a322d8af65cd145f23cc7c0',
    'caseconverter/camel_test.py': '07fa154d7809bea21d3640acfca3650c81be0a1f0f74ed873d7d26584c414b00',
    'caseconverter/caseconverter.py': '31db705ae173c15eb8e737bff9b6ac60a6d745cc0c66800529de6f9ce991ad4d',
    'caseconverter/caseconverter_test.py': '5aa9f555895b46a4633fc3241f0fa2ab13f6e555d46d1268c9ded1354f6f1036',
    'caseconverter/cobol.py': '105ab5400129929e801c5ac1d87a1fe9b6a7e8ae4b59b341d1b2d8f7aee66fd4',
    'caseconverter/cobol_test.py': '2e58082ac88e738f56566e2cb5d194121ff9591979c4b8c86ecdcee85a1dfb37',
    'caseconverter/flat.py': '97c475387706e4e7df07df2cbfec9414368019b2f22e2693363ffd93ef2fefb1',
    'caseconverter/flat_test.py': 'a4b528f2fd10c2ab3635144f8fc88d91e144e2a90ebd3806663a5183038925b3',
    'caseconverter/kebab.py': 'f94536c488fbcacb7a549b55cb45370b0c648a22128460b7cc46b965972bda90',
    'caseconverter/kebab_test.py': 'd12ae148437ab3d475e4926bc4b1d032f4886d2613327b5dc3c7b901627b9476',
    'caseconverter/macro.py': 'e5961cb37ee225f76255ed189f7275b3b93b6d6fc07120ea8739893120e0737e',
    'caseconverter/macro_test.py': 'b0c06bac432dcebdac8d3f9dfed03b4cdedbbb6ab56bea75089d7b57f64f9afc',
    'caseconverter/pascal.py': '0f680dbe7312be1862f576a87683d8c7400a6ccdd0f2de270eea7080d658119d',
    'caseconverter/pascal_test.py': 'd352353762aab17516b2c12e4c5953aa6252482ee023d4eba186870ead1fe636',
    'caseconverter/snake.py': 'a435f6df3d4dbae75c1e6851d07a11c92c266d41b25e0f8c84f57ba66752cfc0',
    'caseconverter/snake_test.py': 'df7d4fde51c9f5670a64f4749de0e0fcae55941c7420b4066829648e070be8f8',
    'caseconverter/title.py': '1d2478e461bd22e569114eb47824f7c786d1ff91f8834324419baac316fb0d7f',
    'caseconverter/title_test.py': 'f43f492f341ebd295e766a15604c4b18ecc4c73dc3882e3a836159d0542f85bc',
    'setup.py': '4f8df3a2d0bf1d6e4eff43e0a417087bea410bc598799f0d6fdf3b7ec306cb20',
}
def owned(path, name):
    assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}\n', str(path)], text=True).strip() == name

work = Path(sys.argv[1]).resolve()
source = Path('/usr/share/python-case-converter/source')
assert len(expected) == 28
assert {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()} == set(expected)
for relative, digest in expected.items():
    p = source / relative
    assert not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest() == digest, relative
    owned(p, 'python-case-converter')
assert importlib.metadata.version('case-converter') == '1.2.0'
module = Path(caseconverter.__file__).resolve().parent
assert str(module).startswith(('/usr/lib/python3.11/site-packages/', '/usr/lib64/python3.11/site-packages/'))
assert not module.is_relative_to(source) and not module.is_relative_to(work)
package_files = {p.name for p in module.glob('*.py')}
expected_package = {Path(p).name for p in expected if p.startswith('caseconverter/')}
assert len(expected_package) == 20 and package_files == expected_package
for filename in sorted(package_files):
    p = module / filename
    assert not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest() == expected['caseconverter/' + filename]
    owned(p, 'python-case-converter')
assert len(list(module.glob('*_test.py'))) == 9
assert sysconfig.get_config_var('WHEEL_PKG_DIR') == '/usr/share/python-wheels'
seeds = [
    ('python-pip-wheel', 'pip', '23.3.1', 'b84249b90c64756fc793e91e5299a4a20eb62980635406f93219279ad069dfe8'),
    ('python-setuptools', 'setuptools', '68.0.0', 'd66278aaa9bc79e49c8d882ab8fec4f4ae2747cc075605377a26732b4b911b69'),
    ('python-wheel-wheel', 'wheel', '0.40.0', '59bb434c712653c6346b6db52da415ffb71448db777743c04229f306826a1822'),
]
for owner, name, version, digest in seeds:
    wheel = Path('/usr/share/python-wheels') / (name + '-' + version + '-py3-none-any.whl')
    owned(wheel, owner)
    assert hashlib.sha256(wheel.read_bytes()).hexdigest() == digest
    with zipfile.ZipFile(wheel) as z:
        prefix = name + '-' + version + '.dist-info/'
        meta = z.read(prefix + 'METADATA').decode()
        assert '\nName: ' + name + '\n' in meta and '\nVersion: ' + version + '\n' in meta
        assert '\nTag: py3-none-any\n' in z.read(prefix + 'WHEEL').decode()
installed_suite = work / 'installed-suite'
installed_suite.mkdir()
shutil.copy2(source / 'Makefile', installed_suite / 'Makefile')
(installed_suite / 'caseconverter').symlink_to(module, target_is_directory=True)
build_source = work / 'offline-build'
build_source.mkdir()
for relative in expected:
    dst = build_source / relative
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / relative, dst)
print(json.dumps({'installed_module': str(module), 'rpm_owned_original_files': 28,
                  'installed_original_python_files': 20, 'original_test_modules': 9,
                  'boundary': 'Static ownership/source/default identity; real whole defaults run next.'}))
PY
# The original Makefile expands all nine test modules against the symlink to
# the authentic installed RPM package. No copied runtime source shadows it.
cd "$work/installed-suite"
make coverage
# Independently retain the original isolated sdist-to-wheel build default,
# using fresh exact RPM-owned original sources and the fixed offline wheelhouse.
cd "$work/offline-build"
make package
test -s dist/case_converter-1.2.0-py3-none-any.whl
printf '%s\n' 'case-converter installed whole coverage and original isolated offline package defaults passed'
