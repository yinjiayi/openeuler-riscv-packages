# SPDX-License-Identifier: Apache-2.0
Name:           gpart
Version:        0.3
Release:        1%{?dist}
Summary:        Partition table rescue/guessing tool
License:        GPL-2.0-or-later
URL:            https://github.com/baruch/gpart
Source0:        gpart-0.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Partition table rescue/guessing tool

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3-1
- Initial openEuler RISC-V package from the full package inventory.
