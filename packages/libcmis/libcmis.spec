# SPDX-License-Identifier: Apache-2.0
Name:           libcmis
Version:        0.6.3
Release:        1%{?dist}
Summary:        a C/C++ client library for the CMIS protocol
License:        GPL-2.0-or-later
URL:            https://github.com/tdf/libcmis
Source0:        libcmis-0.6.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
a C/C++ client library for the CMIS protocol

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
%license COPYING.GPL
%license COPYING.LGPL
%license COPYING.MPL
%doc README.md
%doc NEWS
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3-1
- Initial openEuler RISC-V package from the full package inventory.
