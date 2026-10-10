# SPDX-License-Identifier: Apache-2.0
Name:           python-dpath
Version:        2.2.0
Release:        1%{?dist}
Summary:        Filesystem-like pathing and searching for Python dictionaries
License:        MIT
URL:            https://github.com/dpath-maintainers/dpath-python
Source0:        dpath-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-nose2
BuildRequires:  python3-hypothesis
BuildRequires:  python3-flake8

%description
Filesystem-like pathing, glob searches and updates for nested Python mappings
and sequences, with no third-party runtime dependencies.

%package -n python3-dpath
Summary:        Filesystem-like pathing and searching for Python dictionaries
Requires:       python3

%description -n python3-dpath
Dpath provides filesystem-like paths, glob searches, updates and merges for
nested Python mappings and sequences.

%prep
%autosetup -p1 -n dpath-python-c8722e6b815bedf4e6aaeea9ccc7d6ff3e9b4f84

%build
PIP_NO_INDEX=1 %{__python3} -m pip wheel --no-deps --no-build-isolation --no-index --wheel-dir dist .

%install
PIP_NO_INDEX=1 %{__python3} -m pip install --no-deps --no-index --ignore-installed --no-compile --root %{buildroot} --prefix %{_prefix} dist/dpath-%{version}-py3-none-any.whl

%check
# Upstream uses one shared random hash seed; record one reproducible target seed.
export PYTHONHASHSEED=1
%{__python3} -m flake8 setup.py dpath/ tests/
%{__python3} -m nose2

%files -n python3-dpath
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/dpath/
%{python3_sitelib}/dpath-%{version}.dist-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.0-1
- Package official fixed source with original nose2/hypothesis and flake8 gates.
