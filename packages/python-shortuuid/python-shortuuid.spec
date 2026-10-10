# SPDX-License-Identifier: Apache-2.0
Name:           python-shortuuid
Version:        1.0.13
Release:        1%{?dist}
Summary:        Concise unambiguous URL-safe UUIDs for Python
License:        BSD-3-Clause
URL:            https://github.com/skorokithakis/shortuuid
Source0:        shortuuid-1.0.13.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-poetry-core
BuildRequires:  python3-pytest
BuildRequires:  python3-wheel

%description
Shortuuid creates concise, unambiguous, URL-safe UUID strings and encodes
or decodes existing UUIDs with configurable alphabets and padding.

%package -n python3-shortuuid
Summary:        Concise unambiguous URL-safe UUIDs for Python
Provides:       python-shortuuid = %{version}-%{release}

%description -n python3-shortuuid
Shortuuid's Python 3 modules and command line interface. The optional Django
field module is included unchanged and requires Django to be separately
available when it is imported.

%prep
%autosetup -p1 -n shortuuid-16374d288c796faa2aee5789ed649c3ed7cdd9be

%build
# Use the original Poetry backend, with preinstalled official dependencies.
%{__python3} -m pip wheel --no-deps --no-build-isolation --no-index --wheel-dir dist .

%install
%{__python3} -m pip install --no-deps --no-index --ignore-installed --no-compile --root %{buildroot} --prefix %{_prefix} dist/shortuuid-%{version}-*.whl

%check
# Current upstream test.yml selects the complete default pytest collection.
# Retain all 19 unchanged unittest cases. --md / --emoji only render reports;
# separate pre-commit authoring checks are not asserted as replicated CI.
%{__python3} -m pytest -v -q

%files -n python3-shortuuid
%license COPYING
%doc README.md CHANGELOG.md
%{_bindir}/shortuuid
%{python3_sitelib}/shortuuid/
%{python3_sitelib}/shortuuid-%{version}.dist-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.13-1
- Onboard the official stable source with its original Poetry backend.
- Preserve all upstream runtime tests and optional Django adapter unchanged.
