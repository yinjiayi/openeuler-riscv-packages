# SPDX-License-Identifier: Apache-2.0
Name:           libgnunetworker
Version:        1.1.1
Release:        1%{?dist}
Summary:        Multithreading with GNUnet
License:        AGPL-3.0
URL:            https://github.com/madmurphy/libgnunetworker
Source0:        libgnunetworker-1.1.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Multithreading with GNUnet

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
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
