# SPDX-License-Identifier: Apache-2.0
Name:           ublksrv
Version:        1.6
Release:        1%{?dist}
Summary:        Userspace daemon part (ublksrv) of the ublk framework
License:        MIT
URL:            https://github.com/ublk-org/ublksrv
Source0:        ublksrv-1.6.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Userspace daemon part (ublksrv) of the ublk framework

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
%license COPYING.LGPL
%license LICENSE
%doc README.rst

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-1
- Initial openEuler RISC-V package from the full package inventory.
