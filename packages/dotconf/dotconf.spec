# SPDX-License-Identifier: Apache-2.0
Name:           dotconf
Version:        1.4.1
Release:        1%{?dist}
Summary:        A C library for parsing configuration files
License:        LGPL-2.1-or-later
URL:            https://github.com/williamh/dotconf
Source0:        dotconf-1.4.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A C library for parsing configuration files

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
