# SPDX-License-Identifier: Apache-2.0
Name:           libflowmanager
Version:        3.0.0
Release:        1%{?dist}
Summary:        This library is designed to facilitate performing flow-based measurement tasks using packet-based inputs, particularly packet trace files
License:        LGPL-3.0-or-later
URL:            https://github.com/LibtraceTeam/libflowmanager
Source0:        libflowmanager-3.0.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
This library is designed to facilitate performing flow-based measurement tasks using packet-based inputs, particularly packet trace files

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
%license COPYING.LESSER
%doc README
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
