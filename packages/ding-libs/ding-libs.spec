# SPDX-License-Identifier: Apache-2.0
Name:           ding-libs
Version:        0.7.0
Release:        1%{?dist}
Summary:        "DING is not GNU" helper libraries for SSSD and FreeIPA
License:        LGPL-3.0-or-later
URL:            https://github.com/SSSD/ding-libs
Source0:        ding-libs-0.7.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
"DING is not GNU" helper libraries for SSSD and FreeIPA

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
%license COPYING.LESSER
%doc README

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
