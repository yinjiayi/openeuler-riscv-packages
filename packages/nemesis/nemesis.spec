# SPDX-License-Identifier: Apache-2.0
Name:           nemesis
Version:        1.8
Release:        1%{?dist}
Summary:        command-line network packet crafting and injection utility
License:        BSD-3-Clause
URL:            https://github.com/libnet/nemesis
Source0:        nemesis-1.8.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
command-line network packet crafting and injection utility

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8-1
- Initial openEuler RISC-V package from the full package inventory.
