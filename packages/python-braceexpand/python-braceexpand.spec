# SPDX-License-Identifier: Apache-2.0
Name:           python-braceexpand
Version:        0.1.7
Release:        1%{?dist}
Summary:        Bash-style brace expansion for Python
License:        MIT
URL:            https://github.com/trendels/braceexpand
Source0:        braceexpand-0.1.7-fixed.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
Bash-style brace expansion for Python

%package -n python3-braceexpand
Summary:        %{summary}
Requires:       python3
Provides:       python-braceexpand = %{version}-%{release}

%description -n python3-braceexpand
Bash-style brace expansion for Python, including type annotations and the
original upstream doctest and unittest acceptance inputs.

%prep
%autosetup -n braceexpand-bb0c73c7a349477ef80d00da703cc72301a96727 -p1

%build
%py3_build

%install
%py3_install
# Preserve the exact original standalone test for installed-RPM acceptance.
install -Dpm 0644 test_braceexpand.py %{buildroot}%{_datadir}/python-braceexpand/tests/test_braceexpand.py

%check
# Exact two original Makefile test commands, using the fixed target interpreter.
export PYTHONPATH="$PWD/src"
%{__python3} src/braceexpand/__init__.py
%{__python3} test_braceexpand.py

%files -n python3-braceexpand
%license LICENSE
%doc README.md README.rst CHANGELOG.md
%{python3_sitelib}/braceexpand/
%{python3_sitelib}/braceexpand-*.egg-info/
%{_datadir}/python-braceexpand/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.7-1
- Initial package preserving complete original doctest and unittest defaults.
