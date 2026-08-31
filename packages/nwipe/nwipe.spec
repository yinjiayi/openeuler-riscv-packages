# SPDX-License-Identifier: Apache-2.0
Name:           nwipe
Version:        0.42
Release:        3%{?dist}
Summary:        A fork of the dwipe command that will securely erase disks using a variety of recognised methods
License:        GPL-2.0-or-later
URL:            https://github.com/martijnvanbrummelen/nwipe
Source0:        nwipe-0.42.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libconfig-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  parted-devel
BuildRequires:  pkgconf-pkg-config

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

%check
%make_build check

%files
%{_bindir}/nwipe
%{_mandir}/man8/nwipe.8*
%license COPYING
%doc README.md

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.42-3
- Declare the installed binary and compressed manual page explicitly.

* Sun Aug 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.42-2
- Add the ncurses panel, libconfig, libparted, and pkg-config build dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.42-1
- Initial openEuler RISC-V package from the full package inventory.
