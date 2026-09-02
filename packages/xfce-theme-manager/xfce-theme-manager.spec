# SPDX-License-Identifier: Apache-2.0
Name:           xfce-theme-manager
Version:        0.3.9
Release:        2%{?dist}
Summary:        Integrated theme manager for xfce4
License:        GPL-3.0-or-later
URL:            https://github.com/KeithDHedger/Xfce-Theme-Manager
Source0:        xfce-theme-manager-0.3.9.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Integrated theme manager for xfce4

%prep
%autosetup -n Xfce-Theme-Manager-%{version} -p1

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
%doc ChangeLog

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.9-2
- Match %%prep to the case-sensitive top-level directory in the verified archive.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.9-1
- Initial openEuler RISC-V package from the full package inventory.
