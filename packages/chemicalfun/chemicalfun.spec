# SPDX-License-Identifier: Apache-2.0
Name:           chemicalfun
Version:        0.1.13
Release:        1%{?dist}
Summary:        C++ library (Python and C++ API) for generating balanced chemical reactions and for parsing and calculating properties of chemical formulas
License:        LGPL-2.1-or-later
URL:            https://github.com/thermohub/chemicalfun
Source0:        chemicalfun-0.1.13.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ library (Python and C++ API) for generating balanced chemical reactions and for parsing and calculating properties of chemical formulas

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.13-1
- Initial openEuler RISC-V package from the full package inventory.
