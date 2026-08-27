# SPDX-License-Identifier: Apache-2.0
Name:           libstaroffice
Version:        0.0.8
Release:        1%{?dist}
Summary:        filter for old StarOffice documents(.sdc, .sdw, ...) based on librevenge
License:        LGPL-2.1-or-later
URL:            https://github.com/fosnola/libstaroffice
Source0:        libstaroffice-0.0.8.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
filter for old StarOffice documents(.sdc, .sdw, ...) based on librevenge

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
%license COPYING.LGPL
%license COPYING.MPL
%doc README
%doc NEWS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.8-1
- Initial openEuler RISC-V package from the full package inventory.
