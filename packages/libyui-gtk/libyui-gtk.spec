# SPDX-License-Identifier: Apache-2.0
Name:           libyui-gtk
Version:        2.52.5
Release:        1%{?dist}
Summary:        Gtk3 User Interface for libyui
License:        LGPL-3.0-or-later
URL:            https://github.com/libyui/libyui-gtk
Source0:        libyui-gtk-2.52.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Gtk3 User Interface for libyui

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
%license COPYING.lgpl-2.1
%license COPYING.lgpl-3
%doc README
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.52.5-1
- Initial openEuler RISC-V package from the full package inventory.
