# SPDX-License-Identifier: Apache-2.0
Name:           libason
Version:        0.1.2
Release:        1%{?dist}
Summary:        A library for manipulating ASON values
License:        GPL-3.0-or-later
URL:            https://github.com/sadmac7000/libason
Source0:        libason-0.1.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A library for manipulating ASON values

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
%doc NEWS.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
