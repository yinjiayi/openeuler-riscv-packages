# SPDX-License-Identifier: Apache-2.0
Name:           libldm
Version:        0.2.5
Release:        1%{?dist}
Summary:        A tool and library for managing Microsoft Windows Dynamic Disks
License:        GPL-3.0-or-later
URL:            https://github.com/mdbooth/libldm
Source0:        libldm-0.2.5.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A tool and library for managing Microsoft Windows Dynamic Disks

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
%license COPYING.gpl
%license COPYING.lgpl
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.5-1
- Initial openEuler RISC-V package from the full package inventory.
