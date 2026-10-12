# SPDX-License-Identifier: Apache-2.0
Name:           python-pyuca
Version:        1.2
Release:        1%{?dist}
Summary:        Unicode Collation Algorithm implementation for Python
License:        MIT AND Unicode-DFS-2015
URL:            https://github.com/jtauber/pyuca
Source0:        python-pyuca-1.2.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-flake8
BuildRequires:  python3-coverage
Requires:       python3
Requires:       python3-flake8
Requires:       python3-coverage
BuildArch:      noarch

%description
Pyuca implements the Unicode Collation Algorithm. The complete fixed official
release, original test commands and full Unicode conformance fixtures remain
unchanged. Both upstream copyright and data-license notices are retained.

%prep
%autosetup -n pyuca-d751d694a90ab9d8789263822e02ae822d251e2c

%build
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
python3 setup.py build

%install
python3 setup.py install --skip-build --root %{buildroot} --prefix %{_prefix}
install -d %{buildroot}%{_datadir}/%{name}/original
tar -xf %{SOURCE0} --strip-components=1 -C %{buildroot}%{_datadir}/%{name}/original
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/upstream.tar.gz

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
# Isolate generated build/lib from the unchanged whole original lint/defaults.
check_dir=$(mktemp -d)
tar -xf %{SOURCE0} --strip-components=1 -C "$check_dir"
cd "$check_dir"
flake8 .
coverage run --branch --source pyuca test.py
coverage run --append --branch --source pyuca -m doctest pyuca/utils.py
coverage run --append --branch --source pyuca full_test.py
coverage report

%files
%license LICENSE LICENSE-allkeys
%doc README.md AUTHORS CONTRIBUTING.md
%{python3_sitelib}/pyuca/
%{python3_sitelib}/pyuca-*.egg-info/
%{_datadir}/%{name}/

%changelog
* Mon Oct 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2-1
- Pin the complete official release and preserve all original default checks.
