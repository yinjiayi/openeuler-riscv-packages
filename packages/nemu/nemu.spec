# SPDX-License-Identifier: Apache-2.0
Name:           nemu
Version:        3.4.0
Release:        1%{?dist}
Summary:        ncurses interface for QEMU
License:        BSD-2-Clause
URL:            https://github.com/nemuTUI/nemu
Source0:        nemu-3.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
ncurses interface for QEMU

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
