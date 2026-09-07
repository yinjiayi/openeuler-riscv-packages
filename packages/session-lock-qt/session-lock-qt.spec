# SPDX-License-Identifier: Apache-2.0
Name:           session-lock-qt
Version:        2.1.0
Release:        3%{?dist}
Summary:        session-lock-qt
License:        GPL-3.0-or-later
URL:            https://github.com/waycrate/qt-session-lock
Source0:        session-lock-qt-2.1.0.tar.gz
Patch0:         0001-find-qt-wayland-private-target-via-public-component.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libxkbcommon-devel
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel

%description
session-lock-qt

%prep
%autosetup -n qt-session-lock-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON \
    -DQT_QML_DIR=%{_libdir}/qt6/qml
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure
test -x %{_vpath_builddir}/sessionlock-test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.0-3
- Load the Qt Wayland private target through the public component exported by Qt 6.5.
- Add the XKB provider and verify that the upstream session-lock executable is built.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.0-2
- Match the official archive root and add the required Qt 6 and Wayland development files.
- Install the QML module under the target architecture's library directory.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
