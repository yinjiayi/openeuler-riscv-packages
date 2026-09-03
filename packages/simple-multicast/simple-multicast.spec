# SPDX-License-Identifier: Apache-2.0
Name:           simple-multicast
Version:        0.2.5.2
Release:        1%{?dist}
Summary:        Multicast Server and Client application
License:        GPL-3.0-or-later
URL:            https://github.com/anubisg1/simple-multicast
Source0:        simple-multicast-0.2.5.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Multicast Server and Client application

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.5.2-1
- Initial openEuler RISC-V package from the full package inventory.
