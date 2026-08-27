# SPDX-License-Identifier: Apache-2.0
Name:           mlfbdplugin
Version:        2.0.1
Release:        1%{?dist}
Summary:        MyLibrary plugin for fbd format files creation
License:        GPL-3.0-or-later
URL:            https://github.com/ProfessorNavigator/mlfbdplugin
Source0:        mlfbdplugin-2.0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
MyLibrary plugin for fbd format files creation

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
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
