# SPDX-License-Identifier: Apache-2.0
Name:           python-addict
Version:        2.4.0
Release:        1%{?dist}
Summary:        Dictionary supporting attribute and item syntax
License:        MIT
URL:            https://github.com/mewwts/addict
Source0:        addict-2.4.0-fixed.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-coverage
%description
Dictionary supporting attribute and item syntax.

%package -n python3-addict
Summary:        %{summary}
Requires:       python3
# Retain the original pytest acceptance against the installed package.
Requires:       python3-pytest
Provides:       python-addict = %{version}-%{release}

%description -n python3-addict
Dictionary supporting attribute and item syntax, including the unchanged
original acceptance suite for installed package verification.

%prep
%autosetup -n addict-338936265dd924ec5892aeee9c122d7e4f77680d -p1

%build
%py3_build

%install
%py3_install
install -Dpm 0644 test_addict.py %{buildroot}%{_datadir}/python-addict/tests/test_addict.py

%check
export PYTHONPATH="$PWD"
# Complete original GitHub workflow collection, plus documented unittest CLI.
%{__python3} -m pytest
# Original Travis source-side test_suite loader and coverage command.
export COVERAGE_FILE="$PWD/.coverage-rpm-check"
test ! -e "$COVERAGE_FILE"
%{__python3} -m coverage run --source=addict setup.py test
%{__python3} -m unittest -v test_addict

%files -n python3-addict
%license LICENSE
%doc README.md
%{python3_sitelib}/addict/
%{python3_sitelib}/addict-*.egg-info/
%{_datadir}/python-addict/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.0-1
- Initial package preserving complete upstream pytest and unittest defaults.
