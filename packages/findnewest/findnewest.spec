# SPDX-License-Identifier: Apache-2.0
Name:           findnewest
Version:        0.3
Release:        1%{?dist}
Summary:        Recursively find newest file in a hierarchy and print its timestamp
License:        BSD-2-Clause
URL:            https://github.com/0-wiz-0/findnewest
Source0:        findnewest-0.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Recursively find newest file in a hierarchy and print its timestamp

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3-1
- Initial openEuler RISC-V package from the full package inventory.
