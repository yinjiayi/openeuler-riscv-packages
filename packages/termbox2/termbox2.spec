# SPDX-License-Identifier: Apache-2.0
Name:           termbox2
Version:        2.5.0
Release:        1%{?dist}
Summary:        terminal I/O library
License:        MIT
URL:            https://github.com/termbox/termbox2
Source0:        termbox2-2.5.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
terminal I/O library

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
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
