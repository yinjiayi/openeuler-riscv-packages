# SPDX-License-Identifier: Apache-2.0
Name:           termux-elf-cleaner
Version:        3.0.1
Release:        1%{?dist}
Summary:        Utility to remove unused ELF sections causing warnings
License:        GPL-3.0-or-later
URL:            https://github.com/termux/termux-elf-cleaner
Source0:        termux-elf-cleaner-3.0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Utility to remove unused ELF sections causing warnings

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
