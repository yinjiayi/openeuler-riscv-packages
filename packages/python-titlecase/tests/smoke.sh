#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-titlecase python3-regex python3-coverage
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH
test_root=/usr/share/python-titlecase/source
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
python3 - <<'PY'
import ast
import hashlib
import importlib.metadata
from pathlib import Path
import subprocess
import titlecase

assert importlib.metadata.version('titlecase') == '2.4.1'
assert titlecase.__version__ == '2.4.1' and titlecase.REGEX_AVAILABLE is True
module = Path(titlecase.__file__).resolve()
assert str(module).startswith('/usr/lib/') and module.parent.name == 'titlecase' and module.name == '__init__.py'
owned = Path('/usr/share/python-titlecase/source')
expected = {
    '.github/workflows/ci.yml': 'b1361cc79fb5e5633c8c22da4ddfaa9ba23d24ae5581a2bf50938f992bc8e5f0',
    '.github/workflows/coverage.yml': 'b5e70c89fe6be95305f808ef85809f33aac892d9300348d6dee928e5e0c53ea1',
    '.gitignore': '73d340005f08b52cd8036013a736a2e096a7d7421f5d3fc33a245c5e979fbd06',
    'AUTHORS.rst': '663a8975b87eb5900097c166ae1e7679f385d1f7b248431796cedd75d2056e58',
    'LICENSE.txt': '7e31e4b97035a307b2cef4523674dc1b502c5de57387d713e918a9885a6f33f8',
    'README.rst': '08b4083515b545d3fa92fe6293fec96383f9e6d78739bf4d33e2c7bc73d8be21',
    'pyproject.toml': '2c9479f11b223042d14fb7182f5e67675092144f8c5aad104fd820b9903feb18',
    'setup.cfg': '96e5c0d78f62c8ecb7549068af369821dbb58e5fccab300e8ad1aa20c3a7f6cc',
    'setup.py': '4a096172f786f028c61a02e97e333e4927e45b82d444ea55b625ee9d94e3df03',
    'titlecase/__init__.py': 'd00a7ab438dc481853d2c9f144387b2450c3b67ab4245b94fb43b8508b0f5baa',
    'titlecase/tests.py': 'aa1f041c40c96c49782f0f9b109e28e96eba42fe11652401caaf4a5675eb94c8',
    'tox.ini': 'e117997ba6750902e4bbe4a0d07b4dbd836dd1cfa80c51788374a44da6bb519b',
}
actual = {}
for path in sorted(owned.rglob('*')):
    assert not path.is_symlink()
    if path.is_file():
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(path)], text=True) == 'python-titlecase'
        actual[str(path.relative_to(owned))] = hashlib.sha256(path.read_bytes()).hexdigest()
assert actual == expected
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(module)], text=True) == 'python-titlecase'
assert module.read_bytes() == (owned / 'titlecase/__init__.py').read_bytes()
suite = owned / 'titlecase/tests.py'
assert suite.read_bytes() == (module.parent / 'tests.py').read_bytes()
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(module.parent / 'tests.py')], text=True) == 'python-titlecase'
tree = ast.parse(suite.read_bytes())
assert sum(isinstance(n, ast.FunctionDef) and n.name.startswith('test_') for n in ast.walk(tree)) == 10
data = next(n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'TEST_DATA' for t in n.targets))
assert len(ast.literal_eval(data)) == 72
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', '/usr/bin/titlecase'], text=True) == 'python-titlecase'
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', '/usr/bin/coverage3'], text=True) == 'python3-coverage'
print('Installed RPM-owned Titlecase 2.4.1, exact full 12-file release and 10-method / 72-fixture original suite verified; original skip retained')
PY
# Only original tests are copied; their ../ path insertion cannot find a
# copied titlecase package, so both runs import the installed RPM library.
mkdir "$scratch/tests" "$scratch/no-regex" "$scratch/bin"
ln -s /usr/bin/coverage3 "$scratch/bin/coverage"
export PATH="$scratch/bin:$PATH"
cp "$test_root/titlecase/tests.py" "$scratch/tests/tests.py"
test ! -e "$scratch/titlecase"
cat > "$scratch/no-regex/sitecustomize.py" <<'PY'
import sys
class NoOptionalRegex:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'regex' or fullname.startswith('regex.'):
            raise ModuleNotFoundError('optional regex intentionally absent')
sys.meta_path.insert(0, NoOptionalRegex())
PY
cd "$scratch/tests"
python3 -c 'import titlecase; assert titlecase.REGEX_AVAILABLE is True and titlecase.__file__.startswith("/usr/lib/")'
python3 -m unittest
COVERAGE_FILE="$scratch/coverage-regex" coverage run -m unittest
PYTHONPATH="$scratch/no-regex" python3 -c 'import titlecase; assert titlecase.REGEX_AVAILABLE is False and titlecase.__file__.startswith("/usr/lib/")'
PYTHONPATH="$scratch/no-regex" python3 -m unittest
PYTHONPATH="$scratch/no-regex" COVERAGE_FILE="$scratch/coverage-re" coverage run -m unittest
