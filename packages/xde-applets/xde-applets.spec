# SPDX-License-Identifier: Apache-2.0
Name:           xde-applets
Version:        0.12
Release:        1%{?dist}
Summary:        X Desktop Environment System Tray Icons and Dock Apps
License:        GPL-3.0-or-later
URL:            https://github.com/bbidulock/xde-applets
Source0:        xde-applets-0.12.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
X Desktop Environment System Tray Icons and Dock Apps

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
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12-1
- Initial openEuler RISC-V package from the full package inventory.
