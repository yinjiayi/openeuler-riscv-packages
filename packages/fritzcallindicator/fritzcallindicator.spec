# SPDX-License-Identifier: Apache-2.0
Name:           fritzcallindicator
Version:        0.9.0
Release:        1%{?dist}
Summary:        Show taskbar notifications for incoming calls from the Fritz!Box.
License:        GPL-3.0-or-later
URL:            https://github.com/ElTh0r0/fritzcallindicator
Source0:        fritzcallindicator-0.9.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Show taskbar notifications for incoming calls from the Fritz!Box.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.0-1
- Initial openEuler RISC-V package from the full package inventory.
