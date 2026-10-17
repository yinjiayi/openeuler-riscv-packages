# SPDX-License-Identifier: Apache-2.0
Name:           python-pytrie
Version:        0.4.0
Release:        1%{?dist}
Summary:        Pure Python trie mappings with prefix lookup
License:        BSD-3-Clause AND BSD-2-Clause AND MIT
URL:            https://github.com/gsakkis/pytrie
Source0:        pytrie-0.4.0.tar.gz
Source1:        Sphinx-1.5-LICENSE
Source2:        Sphinx-1.5-AUTHORS
Source3:        jquery-3.1.0-LICENSE.txt
Source4:        Pygments-2.1.3-LICENSE
Source5:        Pygments-2.1.3-AUTHORS
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-sortedcontainers

%description
PyTrie implements trie mappings and prefix lookups in pure Python.

%package -n python3-pytrie
Summary:        Pure Python trie mappings with prefix lookup
Provides:       python-pytrie = %{version}-%{release}
Requires:       python3-sortedcontainers

%description -n python3-pytrie
Python 3 trie mappings, sorted keys and longest-prefix lookups.

%prep
%autosetup -p1 -n pytrie-d88f261d4e9c7046233f005034d7e15575bd30df
# Preserve every upstream file and supplement missing embedded-resource notices.
cp %{SOURCE1} Sphinx-1.5-LICENSE
cp %{SOURCE2} Sphinx-1.5-AUTHORS
cp %{SOURCE3} jquery-3.1.0-LICENSE.txt
cp %{SOURCE4} Pygments-2.1.3-LICENSE
cp %{SOURCE5} Pygments-2.1.3-AUTHORS

%build
# Retain upstream's setuptools backend, using only prepared target RPMs.
%{__python3} setup.py bdist_wheel

%install
set -- dist/*.whl
test "$#" -eq 1
test -f "$1"
%{__python3} -m pip install --no-deps --no-index --ignore-installed --no-compile --root %{buildroot} --prefix %{_prefix} "$1"

%check
# Exact upstream test_suite='tests': retain both modules and inherited mapping cases.
# python3-devel supplies the target CPython test.mapping_tests module.
%{__python3} setup.py test

%files -n python3-pytrie
%license LICENSE Sphinx-1.5-LICENSE Sphinx-1.5-AUTHORS jquery-3.1.0-LICENSE.txt Pygments-2.1.3-LICENSE Pygments-2.1.3-AUTHORS
%doc README.md docs/build/html
%{python3_sitelib}/pytrie.py
%{python3_sitelib}/__pycache__/pytrie.*.pyc
%{python3_sitelib}/PyTrie-%{version}.dist-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Onboard official immutable source with complete original default tests.
- Preserve embedded docs and supplement exact official third-party notices.
