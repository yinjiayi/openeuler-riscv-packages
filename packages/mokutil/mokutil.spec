# SPDX-License-Identifier: Apache-2.0
Name:           mokutil
Version:        0.7.2
Release:        1%{?dist}
Summary:        Shim.efi Machine Owner Key management tool
License:        GPL-3.0-or-later
URL:            https://github.com/lcp/mokutil
Source0:        mokutil-0.7.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Shim.efi Machine Owner Key management tool

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.2-1
- Initial openEuler RISC-V package from the full package inventory.
