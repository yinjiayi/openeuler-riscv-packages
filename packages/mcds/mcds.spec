# SPDX-License-Identifier: Apache-2.0
Name:           mcds
Version:        1.10
Release:        1%{?dist}
Summary:        Mutt Carddav search program
License:        GPL-3.0-or-later
URL:            https://github.com/t-brown/mcds
Source0:        mcds-1.10.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Mutt Carddav search program

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
%license LICENSE
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10-1
- Initial openEuler RISC-V package from the full package inventory.
