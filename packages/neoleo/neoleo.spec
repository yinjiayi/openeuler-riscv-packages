# SPDX-License-Identifier: Apache-2.0
Name:           neoleo
Version:        16.0
Release:        1%{?dist}
Summary:        Lightweight curses spreadsheet based on GNU oleo
License:        GPL-2.0-or-later
URL:            https://github.com/blippy/neoleo
Source0:        neoleo-16.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Lightweight curses spreadsheet based on GNU oleo

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 16.0-1
- Initial openEuler RISC-V package from the full package inventory.
