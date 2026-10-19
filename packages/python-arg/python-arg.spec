# SPDX-License-Identifier: Apache-2.0
Name:           python3-arg
Version:        1.0.2
Release:        1
Summary:        Simple argument parser for Python
License:        ISC
URL:            https://codeberg.org/maandree/python-arg
Source0:        https://codeberg.org/maandree/python-arg/archive/%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-rpm-macros
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
Requires:       python3

%description
Python module for short, long, numeric and custom-symbol command-line flags.

%package tests
Summary:        Complete original Python-arg driver for installed replays
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       tar
Requires:       gzip
Requires:       coreutils

%description tests
Checksum-bound whole official source archive for unchanged installed driver replay.

%prep
%autosetup -n python-arg

%build
%make_build PYTHON=python3

%install
make install PYTHON=python3 PYTHONPKGDIR=%{python3_sitelib} DESTDIR=%{buildroot}
python3 -m compileall -q -d %{python3_sitelib} %{buildroot}%{python3_sitelib}
install -d %{buildroot}%{_datadir}/python-arg/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-arg/qa/python-arg-%{version}.tar.gz

%check
make check PYTHON=python3
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
site = pathlib.Path(root + sysconfig.get_path('purelib')).resolve()
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
run_installed_tests '%{buildroot}'

%files
%license LICENSE
%doc README
%{python3_sitelib}/arg.py
%{python3_sitelib}/__pycache__/arg.*.pyc

%files tests
%license LICENSE
%{_datadir}/python-arg/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.0.2-1
- Preserve the complete original driver and verify staged/installed module identity.
