# SPDX-License-Identifier: Apache-2.0
Name:           rehex
Version:        0.64.0
Release:        1%{?dist}
Summary:        A cross-platform (Windows, Linux, macOS) hex editor for reverse engineering, and everything else
License:        GPL-2.0-or-later
URL:            https://github.com/solemnwarning/rehex
Source0:        rehex-0.64.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A cross-platform (Windows, Linux, macOS) hex editor for reverse engineering, and everything else

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.64.0-1
- Initial openEuler RISC-V package from the full package inventory.
