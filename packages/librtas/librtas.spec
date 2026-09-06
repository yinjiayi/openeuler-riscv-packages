# SPDX-License-Identifier: Apache-2.0
Name:           librtas
Version:        2.0.6
Release:        1%{?dist}
Summary:        Libraries to provide access to RTAS calls and RTAS events
License:        LGPL-2.1-or-later
URL:            https://github.com/ibm-power-utilities/librtas
Source0:        librtas-2.0.6.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Libraries to provide access to RTAS calls and RTAS events

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
%license COPYING.LESSER
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.6-1
- Initial openEuler RISC-V package from the full package inventory.
