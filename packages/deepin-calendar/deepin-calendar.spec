# SPDX-License-Identifier: Apache-2.0
Name:           deepin-calendar
Version:        6.5.42
Release:        2%{?dist}
Summary:        Calendar for Deepin Desktop Environment
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dde-calendar
Source0:        deepin-calendar-6.5.42.tar.gz
BuildRequires:  cmake
BuildRequires:  dtkcore-devel
BuildRequires:  dtkgui-devel
BuildRequires:  dtkwidget-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libical-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  qt5-devel

%description
Calendar for Deepin Desktop Environment

%prep
%autosetup -p1 -n dde-calendar-%{version}

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
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.5.42-2
- Match the verified archive root and declare the Qt 5, DTK, and libical build dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.5.42-1
- Initial openEuler RISC-V package from the full package inventory.
