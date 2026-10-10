# SPDX-License-Identifier: Apache-2.0
Name:           cryptmount
Version:        6.4.0
Release:        1%{?dist}
Summary:        Utility allowing an ordinary user to mount an encrypted file system
License:        GPL-2.0-or-later
URL:            https://github.com/rwpenney/cryptmount
Source0:        cryptmount-6.4.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Utility allowing an ordinary user to mount an encrypted file system

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
%doc README.md
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
