# SPDX-License-Identifier: Apache-2.0
Name:           xdelta3-gui
Version:        26.07
Release:        1%{?dist}
Summary:        GUI for xdelta3 application
License:        GPL-3.0-or-later
URL:            https://github.com/AdrianTM/xdelta3-gui
Source0:        xdelta3-gui-26.07.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
GUI for xdelta3 application

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 26.07-1
- Initial openEuler RISC-V package from the full package inventory.
