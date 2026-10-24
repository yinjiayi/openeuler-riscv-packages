# SPDX-License-Identifier: Apache-2.0
Name:           clamav-gui
Version:        1.4.1
Release:        1%{?dist}
Summary:        Graphical user interface for clamav and freshclam with an integrated service menu for Konqueror/Dolphin to scan files directly from your file manager.
License:        GPL-3.0-or-later
URL:            https://github.com/wusel1007/clamav-gui
Source0:        clamav-gui-1.4.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Graphical user interface for clamav and freshclam with an integrated service menu for Konqueror/Dolphin to scan files directly from your file manager.

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
%doc README
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
