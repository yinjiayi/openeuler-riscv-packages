# SPDX-License-Identifier: Apache-2.0
Name:           nwipe
Version:        0.42
Release:        1%{?dist}
Summary:        A fork of the dwipe command that will securely erase disks using a variety of recognised methods
License:        GPL-2.0-or-later
URL:            https://github.com/martijnvanbrummelen/nwipe
Source0:        nwipe-0.42.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A fork of the dwipe command that will securely erase disks using a variety of recognised methods

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

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.42-1
- Initial openEuler RISC-V package from the full package inventory.
