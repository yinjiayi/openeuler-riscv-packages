# SPDX-License-Identifier: Apache-2.0
Name:           python-dotmap
Version:        1.3.30
Release:        1%{?dist}
Summary:        Ordered dynamically expandable dot-access dictionary
License:        MIT
URL:            https://github.com/drgrib/dotmap
Source0:        dotmap-1.3.30.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-pytest
BuildArch:      noarch

%description
DotMap is an ordered, dynamically expandable dot-access dictionary.
The whole original unittest and pytest suite is retained for installed
package acceptance, with no source-library shadow.

%prep
%autosetup -n dotmap-c7a778a95a01a7a0fd2f816a07c62de2478260c6

%build
export PIP_DISABLE_PIP_VERSION_CHECK=1
python3 -m pip wheel --no-build-isolation --no-deps --no-index --wheel-dir dist .

%install
python3 -m pip install --no-index --no-deps --no-compile --root %{buildroot} --prefix %{_prefix} dist/dotmap-%{version}-py3-none-any.whl
install -d %{buildroot}%{_datadir}/%{name}/tests %{buildroot}%{_datadir}/%{name}/reference
install -m 0644 dotmap/test.py %{buildroot}%{_datadir}/%{name}/tests/test.py
install -m 0644 dotmap/__init__.py %{buildroot}%{_datadir}/%{name}/reference/__init__.py
install -m 0644 setup.py setup.cfg MANIFEST.in Makefile requirements.txt .travis.yml %{buildroot}%{_datadir}/%{name}/

%check
# The complete original Makefile test and Travis script, not a subset.
python3 -m unittest
pytest dotmap/test.py

%files
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/dotmap/
%{python3_sitelib}/dotmap-*.dist-info/
%{_datadir}/%{name}/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.30-1
- Pin the official release identity and retain both whole default test gates.
