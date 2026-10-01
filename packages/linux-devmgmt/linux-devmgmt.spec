# SPDX-License-Identifier: Apache-2.0
Name:           linux-devmgmt
Version:        2.1.1
Release:        1%{?dist}
Summary:        A faithful recreation of the Windows Device Manager
License:        GPL-3.0-or-later
URL:            https://github.com/actuallyaridan/linux-devmgmt
Source0:        linux-devmgmt-2.1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A faithful recreation of the Windows Device Manager

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
