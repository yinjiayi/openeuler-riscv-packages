# SPDX-License-Identifier: Apache-2.0
Name:           idu
Version:        0.1.0
Release:        2%{?dist}
Summary:        Instant du -sh and a bit more
License:        MIT
URL:            https://github.com/MkP369/idu
Source0:        idu-0.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Instant du -sh and a bit more

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-2
- Configure explicit CMake source and build directories for the RPM macros.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
