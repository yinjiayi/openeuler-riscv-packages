# SPDX-License-Identifier: Apache-2.0
Name:           libpurple-carbons
Version:        0.2.3
Release:        1%{?dist}
Summary:        Experimental XEP-0280: Message Carbons plugin for libpurple (Pidgin, Finch, etc.)
License:        GPL-2.0-or-later
URL:            https://github.com/gkdr/carbons
Source0:        libpurple-carbons-0.2.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Experimental XEP-0280: Message Carbons plugin for libpurple (Pidgin, Finch, etc.)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.3-1
- Initial openEuler RISC-V package from the full package inventory.
