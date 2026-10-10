# SPDX-License-Identifier: Apache-2.0
Name:           pegtl
Version:        3.2.8
Release:        1%{?dist}
Summary:        Parsing Expression Grammar Template Library
License:        BSL-1.0
URL:            https://github.com/taocpp/PEGTL
Source0:        pegtl-3.2.8.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Parsing Expression Grammar Template Library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.8-1
- Initial openEuler RISC-V package from the full package inventory.
