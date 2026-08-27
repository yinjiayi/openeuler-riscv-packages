# SPDX-License-Identifier: Apache-2.0
Name:           xrestrict
Version:        0.8.0
Release:        1%{?dist}
Summary:        A utility to modify the "Coordinate Transformation Matrix" of an XInput2 device
License:        MIT
URL:            https://github.com/Ademan/xrestrict
Source0:        xrestrict-0.8.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A utility to modify the "Coordinate Transformation Matrix" of an XInput2 device

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.0-1
- Initial openEuler RISC-V package from the full package inventory.
