# SPDX-License-Identifier: Apache-2.0
Name:           iec16022
Version:        0.3.1
Release:        1%{?dist}
Summary:        Produce 2D barcodes often also referenced as DataMatrix
License:        GPL-2.0-or-later
URL:            https://github.com/rdoeffinger/iec16022
Source0:        iec16022-0.3.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Produce 2D barcodes often also referenced as DataMatrix

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
