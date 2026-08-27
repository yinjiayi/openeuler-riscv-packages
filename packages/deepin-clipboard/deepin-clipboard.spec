# SPDX-License-Identifier: Apache-2.0
Name:           deepin-clipboard
Version:        6.1.33
Release:        1%{?dist}
Summary:        DDE clipboard manager component
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dde-clipboard
Source0:        deepin-clipboard-6.1.33.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
DDE clipboard manager component

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.1.33-1
- Initial openEuler RISC-V package from the full package inventory.
