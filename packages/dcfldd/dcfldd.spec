# SPDX-License-Identifier: Apache-2.0
Name:           dcfldd
Version:        1.9.3
Release:        1%{?dist}
Summary:        Enhanced version of dd for forensics and security
License:        GPL-2.0-or-later
URL:            https://github.com/resurrecting-open-source-projects/dcfldd
Source0:        dcfldd-1.9.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Enhanced version of dd for forensics and security

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
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.3-1
- Initial openEuler RISC-V package from the full package inventory.
