# SPDX-License-Identifier: Apache-2.0
Name:           mp3unicode
Version:        1.2.1
Release:        1%{?dist}
Summary:        A command line utility to convert ID3 tags in mp3 files between different encodings
License:        GPL-2.0-or-later
URL:            https://github.com/alonbl/mp3unicode
Source0:        mp3unicode-1.2.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
A command line utility to convert ID3 tags in mp3 files between different encodings

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
