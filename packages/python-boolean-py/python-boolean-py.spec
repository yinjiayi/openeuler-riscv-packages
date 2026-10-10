# SPDX-License-Identifier: Apache-2.0
Name:           python-boolean-py
Version:        5.0
Release:        1%{?dist}
Summary:        Boolean algebra expressions, parsing and simplification for Python
License:        BSD-2-Clause
URL:            https://github.com/bastikr/boolean.py
Source0:        boolean-py-5.0.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest >= 6
BuildRequires:  python3-pytest-xdist >= 2

%description
Boolean algebra expressions, parsing and simplification for Python.

%package -n python3-boolean-py
Summary:        %{summary}
Requires:       python3

%description -n python3-boolean-py
Boolean algebra expressions, parsing and simplification for Python 3.

%prep
%autosetup -p1 -n boolean.py-8a443837e68dc027004294fb17fe1857cf783410

%build
python3 -m pip wheel --no-index --no-build-isolation --no-deps --wheel-dir dist .

%install
python3 -m pip install --no-index --no-deps --ignore-installed --no-compile \
    --root %{buildroot} --prefix %{_prefix} dist/boolean.py-%{version}-py3-none-any.whl

%check
# Retain the upstream testing extra's explicit excluded pytest release.
python3 -c 'import importlib.metadata; assert importlib.metadata.version("pytest") != "7.0.0"'
# Original tox/workflow command; original setup.cfg retains doctests and strict markers.
python3 -m pytest -vvs boolean

%files -n python3-boolean-py
%license LICENSE.txt
%doc README.rst CHANGELOG.rst
%{python3_sitelib}/boolean/
%{python3_sitelib}/boolean.py-%{version}.dist-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.0-1
- Package official fixed-commit source with the original pytest and doctest suite.
