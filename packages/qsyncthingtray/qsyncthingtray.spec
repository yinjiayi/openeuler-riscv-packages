# SPDX-License-Identifier: Apache-2.0
Name:           qsyncthingtray
Version:        0.5.8
Release:        1%{?dist}
Summary:        Qt-based Traybar Application for Syncthing
License:        LGPL-3.0-or-later
URL:            https://github.com/sieren/QSyncthingTray
Source0:        qsyncthingtray-0.5.8.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Qt-based Traybar Application for Syncthing

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
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.8-1
- Initial openEuler RISC-V package from the full package inventory.
