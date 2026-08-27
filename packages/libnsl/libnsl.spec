# SPDX-License-Identifier: Apache-2.0
Name:           libnsl
Version:        2.0.1
Release:        1%{?dist}
Summary:        Public client interface library for NIS(YP)
License:        LGPL-2.1-or-later
URL:            https://github.com/thkukuk/libnsl
Source0:        libnsl-2.0.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Public client interface library for NIS(YP)

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
