# SPDX-License-Identifier: Apache-2.0
Name:           htop
Version:        3.5.2
Release:        1%{?dist}
Summary:        Interactive process viewer
License:        GPL-2.0-or-later
URL:            https://htop.dev
Source0:        htop-3.5.2.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pkgconf-pkg-config

%description
Interactive process viewer

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc README.md
%{_bindir}/htop
%{_datadir}/applications/htop.desktop
%{_datadir}/icons/hicolor/scalable/apps/htop.svg
%{_datadir}/pixmaps/htop.png
%{_mandir}/man1/htop.1*

%changelog
* Sun Aug 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.5.2-1
- Package the official htop 3.5.2 release for openEuler RISC-V.
- Preserve the upstream make check suite and installed desktop integration.
