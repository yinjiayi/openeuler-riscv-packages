# SPDX-License-Identifier: Apache-2.0
Name:           ndstool
Version:        2.3.1
Release:        1%{?dist}
Summary:        A tool for packing and unpacking nds roms
License:        GPL-3.0-or-later
URL:            https://github.com/devkitPro/ndstool
Source0:        ndstool-2.3.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
A tool for packing and unpacking nds roms

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
