# SPDX-License-Identifier: Apache-2.0
Name:           roll
Version:        2.7.0
Release:        1%{?dist}
Summary:        A tool to roll a user-defined dice sequence and display the result
License:        GPL-2.0-or-later
URL:            https://github.com/matteocorti/roll
Source0:        roll-2.7.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A tool to roll a user-defined dice sequence and display the result

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%license COPYRIGHT
%doc README.md
%doc NEWS.md
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
