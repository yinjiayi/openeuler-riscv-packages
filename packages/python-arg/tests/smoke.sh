#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/python-arg/qa/python-arg-1.0.2.tar.gz"
    echo 'def24fe254a2e1a649366151e362e83ab7d1983b0187c057f20f6f60e0d3b04d  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cd "$work"
    # Isolated Python ignores ambient PYTHONPATH and does not add the QA directory.
    python3 -I -B - "$root" "$work/test.py" <<'PY'
import hashlib, pathlib, runpy, sys, sysconfig
root, driver = sys.argv[1:]
assert not sys.flags.optimize
# The runtime's default scheme may be /usr/local; this RPM is installed in /usr.
purelib = sysconfig.get_path('purelib', scheme='posix_prefix', vars={'base': '/usr', 'platbase': '/usr'})
site = pathlib.Path(root + purelib).resolve()
assert site == pathlib.Path(root + '/usr/lib/python' + sysconfig.get_python_version() + '/site-packages').resolve()
sys.path.insert(0, str(site))
import arg
module = pathlib.Path(arg.__file__).resolve()
assert module == site / 'arg.py', module
assert hashlib.sha256(module.read_bytes()).hexdigest() == '07f1dde6a3ef5a4d2ed639bcd25ad0347b1eeb94f77fa9320dad12a6bfb9593f'
print('PASS installed module identity, official digest and enabled assertions', flush=True)
sys.argv = [driver]
runpy.run_path(driver, run_name='__main__')
PY
    echo 'PASS python-arg unchanged complete upstream driver against installed module'
)
run_installed_tests ''
