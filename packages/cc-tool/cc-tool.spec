# SPDX-License-Identifier: Apache-2.0
Name:           cc-tool
Version:        0.27
Release:        1%{?dist}
Summary:        Programmer for Texas Instruments 8051-based System-On-Chip devices
License:        GPL-2.0-or-later
URL:            https://github.com/dashesy/cc-tool
Source0:        cc-tool-0.27.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Programmer for Texas Instruments 8051-based System-On-Chip devices

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.27-1
- Initial openEuler RISC-V package from the full package inventory.
