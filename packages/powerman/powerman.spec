# SPDX-License-Identifier: Apache-2.0
Name:           powerman
Version:        2.4.4
Release:        1%{?dist}
Summary:        Centralized Power Control for Clusters
License:        GPL-2.0-or-later
URL:            https://github.com/chaos/powerman
Source0:        powerman-2.4.4.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Centralized Power Control for Clusters

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
%doc NEWS.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.4-1
- Initial openEuler RISC-V package from the full package inventory.
