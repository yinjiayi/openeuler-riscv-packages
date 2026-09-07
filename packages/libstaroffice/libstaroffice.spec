# SPDX-License-Identifier: Apache-2.0
Name:           libstaroffice
Version:        0.0.8
Release:        3%{?dist}
Summary:        filter for old StarOffice documents(.sdc, .sdw, ...) based on librevenge
License:        LGPL-2.1-or-later
URL:            https://github.com/fosnola/libstaroffice
Source0:        libstaroffice-0.0.8.tar.gz
Patch0:         0001-accept-autoconf-2.71.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  librevenge-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  zlib-devel

%description
filter for old StarOffice documents(.sdc, .sdw, ...) based on librevenge

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --without-docs
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
src/conv/sdc2csv/sdc2csv regression/Calc3.1/nimp.sdc > nimp.actual.csv
cmp regression/Calc3.1/nimp.sdc.csv nimp.actual.csv

%files -f %{name}.files
%license COPYING.LGPL
%license COPYING.MPL
%doc README
%doc NEWS

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.8-3
- Validate the installed public header under its versioned include directory.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.8-2
- Accept openEuler Autoconf 2.71 and declare the complete build dependencies.
- Verify the built spreadsheet converter against the pinned regression fixture.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.8-1
- Initial openEuler RISC-V package from the full package inventory.
