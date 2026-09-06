# SPDX-License-Identifier: Apache-2.0
Name:           libnet
Version:        1.3
Release:        1%{?dist}
Summary:        A library which provides API for commonly used low-level net functions
License:        BSD-2-Clause
URL:            https://github.com/libnet/libnet
Source0:        libnet-1.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A library which provides API for commonly used low-level net functions

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3-1
- Initial openEuler RISC-V package from the full package inventory.
