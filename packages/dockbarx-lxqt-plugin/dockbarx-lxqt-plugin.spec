# SPDX-License-Identifier: Apache-2.0
Name:           dockbarx-lxqt-plugin
Version:        0.9.4
Release:        1%{?dist}
Summary:        DockBarX LXQT applet
License:        GPL-3.0-or-later
URL:            https://github.com/xuzhen/dockbarx-lxqt-plugin
Source0:        dockbarx-lxqt-plugin-0.9.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
DockBarX LXQT applet

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.4-1
- Initial openEuler RISC-V package from the full package inventory.
