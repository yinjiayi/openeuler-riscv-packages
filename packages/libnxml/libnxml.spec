# SPDX-License-Identifier: Apache-2.0
Name:           libnxml
Version:        0.18.5
Release:        1%{?dist}
Summary:        nXML is a C library for parsing, writing and creating XML 1.0 and 1.1 documents
License:        LGPL-2.1-or-later
URL:            https://github.com/bakulf/libnxml
Source0:        libnxml-0.18.5.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
nXML is a C library for parsing, writing and creating XML 1.0 and 1.1 documents

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.18.5-1
- Initial openEuler RISC-V package from the full package inventory.
