# SPDX-License-Identifier: Apache-2.0
Name:           python-simpleeval
Version:        1.0.8
Release:        1%{?dist}
Summary:        Single-expression evaluator for Python
License:        MIT
URL:            https://github.com/danthedeckie/simpleeval
Source0:        python-simpleeval-1.0.8.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-hatchling
BuildRequires:  python3-coverage
Requires:       python3
Requires:       python3-coverage
BuildArch:      noarch

%description
Simpleeval evaluates a single expression with configurable names, operators and
functions. It is not a general sandbox or a guarantee against resource abuse.
The fixed official release, MIT notices, complete original tests and their
original target-interpreter commands remain unchanged.

%prep
%autosetup -n simpleeval-e4466b7a69f8e7420dbce003d99f5e8c0562367c

%build
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
# ZIP timestamps begin in 1980; use the accepted fixed Hatchling wheel epoch.
SOURCE_DATE_EPOCH=315532800 python3 -m pip wheel --no-deps --no-build-isolation --no-index --wheel-dir dist .

%install
python3 -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix %{_prefix} dist/simpleeval-1.0.8-*.whl
install -d %{buildroot}%{_datadir}/%{name}/original
tar -xf %{SOURCE0} --strip-components=1 -C %{buildroot}%{_datadir}/%{name}/original
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/upstream.tar.gz

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
# Generated wheel/build outputs cannot enter unchanged original collection.
check_dir=$(mktemp -d)
tar -xf %{SOURCE0} --strip-components=1 -C "$check_dir"
cd "$check_dir"
python3 -Werror -m unittest
# Official coverage provides its cmdline through this module, not a bare CLI.
python3 -m coverage run -m unittest
python3 -m coverage xml

%files
%license LICENCE
%doc README.rst
%{python3_sitelib}/simpleeval.py
%{python3_sitelib}/__pycache__/simpleeval*.pyc
%{python3_sitelib}/simpleeval-*.dist-info/
%{_datadir}/%{name}/

%changelog
* Mon Oct 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.8-1
- Pin the full official release and preserve complete target-interpreter tests.
