# SPDX-License-Identifier: Apache-2.0
%global upstream_commit bfdd3f6cf86934f2c3318dd949676aa382be4a89
Name:           python-expandvars
Version:        1.1.2
Release:        1%{?dist}
Summary:        Expand environment variables with Unix shell-style syntax
License:        MIT
URL:            https://github.com/sayanarijit/expandvars
Source0:        expandvars-1.1.2.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-hatchling
BuildRequires:  python3-pip
BuildRequires:  python3-black
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov

%description
A pure Python implementation of Unix shell-style environment-variable
expansion. The complete original tests, fixture and coverage threshold are
preserved; the original Black diff diagnostic is also retained.

%package -n python3-expandvars
Summary:        %{summary}
Provides:       python-expandvars = %{version}-%{release}
Requires:       python3
Requires:       python3-black
Requires:       python3-pytest
Requires:       python3-pytest-cov

%description -n python3-expandvars
The library and RPM-owned complete upstream test contract. Black and pytest
are support for installed acceptance, not library runtime dependencies.

%prep
%autosetup -n expandvars-%{upstream_commit}

%build
# Wheel ZIP timestamps start in 1980; keep a fixed epoch only for this backend.
SOURCE_DATE_EPOCH=315532800 python3 -m hatchling build -t wheel

%install
python3 -m pip install --no-index --no-deps --no-compile --root %{buildroot} --prefix %{_prefix} dist/expandvars-%{version}-py3-none-any.whl
mkdir -p %{buildroot}%{_datadir}/python-expandvars/tests/reference
cp -a tests %{buildroot}%{_datadir}/python-expandvars/tests/
install -m 0644 pyproject.toml tox.ini uv.lock %{buildroot}%{_datadir}/python-expandvars/tests/
install -m 0644 expandvars.py %{buildroot}%{_datadir}/python-expandvars/tests/reference/expandvars.py

%check
# Exact complete upstream tox command sequence; no test selection or waiver.
black --diff .
PYTHONPATH=. python3 -m pytest --cov --cov-report=html --cov-fail-under=100

%files -n python3-expandvars
%license LICENSE
%doc README.md
%{python3_sitelib}/expandvars.py
%{python3_sitelib}/expandvars-*.dist-info/
%{_datadir}/python-expandvars/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.2-1
- Package official fixed stable release and unchanged full test contract.
