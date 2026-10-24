# SPDX-License-Identifier: Apache-2.0
Name:           python-aenum
Version:        3.1.17
Release:        1%{?dist}
Summary:        Advanced enumerations, named tuples and named constants
License:        BSD-3-Clause AND Python-2.0
URL:            https://github.com/ethanfurman/aenum
Source0:        aenum-3.1.17-fixed.tar.gz
Source1:        aenum-3.1.17.tar.gz
Source2:        cpython-LICENSE.txt
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pyparsing

%description
Advanced enumerations compatible with Python's standard enum, together with
named tuples and named constants.

%package -n python3-aenum
Summary:        %{summary}
Requires:       python3
# The original default test_v3 suite optionally imports this parser.
Requires:       python3-pyparsing
Provides:       python-aenum = %{version}-%{release}

%description -n python3-aenum
Advanced enumerations compatible with Python's standard enum, together with
named tuples and named constants.

%prep
%autosetup -n aenum-f0f6fd8e2ac0bb379eb11f6029023d2bad88732a -p1
# Restore only the two release document files absent from the Git tree.
# The PyPI README is byte-identical to the original Git root README.
tar -xOf %{SOURCE1} aenum-3.1.17/aenum/README.md > aenum/README.md
tar -xOf %{SOURCE1} aenum-3.1.17/aenum/doc/aenum.pdf > aenum/doc/aenum.pdf
# Conservative full notice restoration; exact copied CPython revision unknown.
cp -p %{SOURCE2} cpython-LICENSE.txt

%build
%py3_build

%install
# Original Python3 install drops source _py2.py, but --skip-build retains its
# generated copy from the preceding build. Remove only that stale build output.
rm -f -- build/lib/aenum/_py2.py
%py3_install

%check
# Original module-main retains tempdir and load_tests/doctest gates.
%{__python3} -m aenum.test

%files -n python3-aenum
%license aenum/LICENSE cpython-LICENSE.txt
%doc README.md aenum/CHANGES
%{python3_sitelib}/aenum/
%{python3_sitelib}/aenum-*.egg-info/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.17-1
- Initial package preserving upstream defaults and original release documents.
