# SPDX-License-Identifier: Apache-2.0
Name:           python-string-utils
Version:        1.0.0
Release:        1%{?dist}
Summary:        String validation, manipulation and generation utilities for Python
License:        MIT
URL:            https://github.com/daveoncode/python-string-utils
Source0:        python-string-utils-1.0.0.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
Requires:       python3
# Installed smoke replays the original build script in a fresh private tree.
Requires:       python3-setuptools
Requires:       python3-wheel
BuildArch:      noarch

%description
String Utils provides validation, manipulation, compression and generation
helpers using the Python standard library. The complete official release,
original test suite and default configuration are retained unchanged.

%prep
%autosetup -n python-string-utils-d903db3c24de35c5cb7e1229ebbcc19775a952a8

%build
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
# Keep build.sh byte-for-byte and its literal python command. Bind that
# executable to the fixed target Python rather than a historical interpreter.
install -d %{_builddir}/%{name}-python
ln -s /usr/bin/python3 %{_builddir}/%{name}-python/python
PATH="%{_builddir}/%{name}-python:$PATH" bash build.sh

%install
python3 setup.py install --skip-build --root %{buildroot} --prefix %{_prefix}
# Namespace-safe packaging relocation; upstream source/default remains intact.
install -d %{buildroot}%{_docdir}/%{name}
mv %{buildroot}%{_prefix}/README/README.md %{buildroot}%{_docdir}/%{name}/README.md
rmdir %{buildroot}%{_prefix}/README
install -d %{buildroot}%{_datadir}/%{name}/tests
install -m 0644 tests/__init__.py tests/test_*.py %{buildroot}%{_datadir}/%{name}/tests/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/upstream.tar.gz

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME
# Original tox default unchanged, whole suite, target Python 3.11 only.
# Neither historical py35-py38 coverage nor local target success is claimed.
PYTHONPATH="$PWD/build/lib" python3 -m unittest

%files
%license LICENSE
%{_docdir}/%{name}/README.md
%{python3_sitelib}/string_utils/
%{python3_sitelib}/python_string_utils-*.egg-info/
%{_datadir}/%{name}/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Pin the complete official release and preserve original default build/tests.
