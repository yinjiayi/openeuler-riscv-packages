# SPDX-License-Identifier: Apache-2.0
Name:           libtranslit
Version:        0.0.3
Release:        1%{?dist}
Summary:        ASCII to Unicode transliteration library with multiple backends
License:        GPL-3.0-or-later
URL:            https://github.com/ueno/libtranslit
Source0:        libtranslit-0.0.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
ASCII to Unicode transliteration library with multiple backends

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
