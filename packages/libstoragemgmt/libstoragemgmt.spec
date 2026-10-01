# SPDX-License-Identifier: Apache-2.0
Name:           libstoragemgmt
Version:        1.10.3
Release:        1%{?dist}
Summary:        A library for storage management
License:        LGPL-2.1-or-later
URL:            https://github.com/libstorage/libstoragemgmt
Source0:        libstoragemgmt-1.10.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A library for storage management

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
%license COPYING.LIB
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10.3-1
- Initial openEuler RISC-V package from the full package inventory.
