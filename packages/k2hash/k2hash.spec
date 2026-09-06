# SPDX-License-Identifier: Apache-2.0
Name:           k2hash
Version:        1.0.100
Release:        1%{?dist}
Summary:        NoSQL Key Value Store(KVS) tools and library
License:        MIT
URL:            https://github.com/yahoojapan/k2hash
Source0:        k2hash-1.0.100.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
NoSQL Key Value Store(KVS) tools and library

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
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.100-1
- Initial openEuler RISC-V package from the full package inventory.
