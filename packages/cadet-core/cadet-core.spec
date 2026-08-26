# SPDX-License-Identifier: Apache-2.0
Name:           cadet-core
Version:        5.1.0
Release:        1%{?dist}
Summary:        Modeling and simulation framework for biotechnology processes – simulation backend
License:        AGPL-3.0
URL:            https://github.com/cadet/cadet-core
Source0:        cadet-core-5.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Modeling and simulation framework for biotechnology processes – simulation backend

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE.txt
%doc README.rst

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
