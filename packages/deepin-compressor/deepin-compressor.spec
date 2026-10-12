# SPDX-License-Identifier: Apache-2.0
Name:           deepin-compressor
Version:        6.5.32
Release:        1%{?dist}
Summary:        A fast and lightweight application for creating and extracting archives
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/deepin-compressor
Source0:        deepin-compressor-6.5.32.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A fast and lightweight application for creating and extracting archives

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.5.32-1
- Initial openEuler RISC-V package from the full package inventory.
