# SPDX-License-Identifier: Apache-2.0
Name:           python-crccheck
Version:        1.3.1
Release:        1%{?dist}
Summary:        Calculation library for CRCs and checksums
License:        MIT
URL:            https://github.com/MartinScharrer/crccheck
Source0:        crccheck-1.3.1.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-setuptools >= 61.2
BuildRequires:  python3-setuptools_scm >= 7
BuildRequires:  python3-tomli
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-coverage

%description
Crccheck implements CRC and checksum calculation algorithms in pure Python.

%package -n python3-crccheck
Summary:        Calculation library for CRCs and checksums
Provides:       python-crccheck = %{version}-%{release}
# The preserved installed upstream regression suite needs coverage.
Requires:       python3-coverage

%description -n python3-crccheck
Python 3 CRC and checksum library, module command line interface, and the
unchanged upstream regression suite for installation verification.

%prep
%autosetup -p1 -n crccheck-%{version}

%build
# Preserve the original PEP 517 backend and sdist SCM version metadata.
%{__python3} -m build --no-isolation

%install
set -- dist/*.whl
test "$#" -eq 1
test -f "$1"
%{__python3} -m pip install --no-deps --no-index --ignore-installed --no-compile --root %{buildroot} --prefix %{_prefix} "$1"
install -d %{buildroot}%{_datadir}/python-crccheck
cp -a tests %{buildroot}%{_datadir}/python-crccheck/tests
install -m 0644 .coveragerc %{buildroot}%{_datadir}/python-crccheck/.coveragerc

%check
# Original Makefile all:test commands, using the target Python 3 interpreter.
# Do not change the original coverage exclusions or random-data tests.
export COVERAGE_FILE="$PWD/.coverage-rpm-check"
%{__python3} -m coverage run --branch -m unittest discover
%{__python3} -m coverage report
%{__python3} -m coverage html

%files -n python3-crccheck
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/crccheck/
%{python3_sitelib}/crccheck-%{version}.dist-info/
%{_datadir}/python-crccheck/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Onboard official release sdist with original backend and complete defaults.
- Retain all upstream tests and coverage configuration for installed smoke.
