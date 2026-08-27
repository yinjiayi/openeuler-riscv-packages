# SPDX-License-Identifier: Apache-2.0
Name:           tty-solitaire
Version:        1.4.1
Release:        1%{?dist}
Summary:        ncurses-based klondike solitaire game
License:        MIT
URL:            https://github.com/mpereira/tty-solitaire
Source0:        tty-solitaire-1.4.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
ncurses-based klondike solitaire game

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
%doc README
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
