# SPDX-License-Identifier: Apache-2.0
Name:           libvpd
Version:        2.2.11
Release:        1%{?dist}
Summary:        VPD Database access library for lsvpd
License:        LGPL-2.1-or-later
URL:            https://github.com/power-ras/libvpd
Source0:        libvpd-2.2.11.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
VPD Database access library for lsvpd

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
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.11-1
- Initial openEuler RISC-V package from the full package inventory.
