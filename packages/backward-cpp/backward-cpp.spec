# SPDX-License-Identifier: Apache-2.0
Name:           backward-cpp
Version:        1.6
Release:        1%{?dist}
Summary:        A beautiful stack trace pretty printer for C++
License:        MIT
URL:            https://github.com/bombela/backward-cpp
Source0:        backward-cpp-1.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A beautiful stack trace pretty printer for C++

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
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-1
- Initial openEuler RISC-V package from the full package inventory.
