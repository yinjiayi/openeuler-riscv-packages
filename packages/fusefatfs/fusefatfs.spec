# SPDX-License-Identifier: Apache-2.0
Name:           fusefatfs
Version:        0.3
Release:        1%{?dist}
Summary:        FUSE/VUOS module for FAT (12/16/32/exFAT)
License:        GPL-2.0-or-later
URL:            https://github.com/virtualsquare/fusefatfs
Source0:        fusefatfs-0.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
FUSE/VUOS module for FAT (12/16/32/exFAT)

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
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3-1
- Initial openEuler RISC-V package from the full package inventory.
