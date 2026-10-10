# SPDX-License-Identifier: Apache-2.0
Name:           libfullock
Version:        1.0.65
Release:        1%{?dist}
Summary:        Fast User Level LOCK (FULLOCK) library for C/C++
License:        MIT
URL:            https://github.com/yahoojapan/fullock
Source0:        libfullock-1.0.65.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Fast User Level LOCK (FULLOCK) library for C/C++

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.65-1
- Initial openEuler RISC-V package from the full package inventory.
