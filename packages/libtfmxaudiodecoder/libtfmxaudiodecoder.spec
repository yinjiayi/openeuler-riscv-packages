# SPDX-License-Identifier: Apache-2.0
Name:           libtfmxaudiodecoder
Version:        1.0.2
Release:        1%{?dist}
Summary:        C wrapper library for TFMX & FC music files
License:        GPL-2.0-or-later
URL:            https://github.com/mschwendt/libtfmxaudiodecoder
Source0:        libtfmxaudiodecoder-1.0.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
C wrapper library for TFMX & FC music files

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

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
