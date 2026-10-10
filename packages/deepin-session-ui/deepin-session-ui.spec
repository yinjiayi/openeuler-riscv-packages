# SPDX-License-Identifier: Apache-2.0
Name:           deepin-session-ui
Version:        6.0.45
Release:        1%{?dist}
Summary:        Deepin desktop-environment - Session UI module
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dde-session-ui
Source0:        deepin-session-ui-6.0.45.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Deepin desktop-environment - Session UI module

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.45-1
- Initial openEuler RISC-V package from the full package inventory.
