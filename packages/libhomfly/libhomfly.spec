# SPDX-License-Identifier: Apache-2.0
Name:           libhomfly
Version:        1.04
Release:        1%{?dist}
Summary:        Library to compute the homfly polynomial of a link
License:        Unlicense
URL:            https://github.com/miguelmarco/libhomfly
Source0:        libhomfly-1.04.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Library to compute the homfly polynomial of a link

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.04-1
- Initial openEuler RISC-V package from the full package inventory.
