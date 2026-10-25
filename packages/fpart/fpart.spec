# SPDX-License-Identifier: Apache-2.0
Name:           fpart
Version:        1.7.0
Release:        1%{?dist}
Summary:        A tool that helps you sort file trees and pack them into bags, like dirsplit
License:        BSD-2-Clause
URL:            https://github.com/martymac/fpart
Source0:        fpart-1.7.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A tool that helps you sort file trees and pack them into bags, like dirsplit

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
