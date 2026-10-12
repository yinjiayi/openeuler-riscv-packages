# SPDX-License-Identifier: Apache-2.0
Name:           libaiff
Version:        6.0
Release:        1%{?dist}
Summary:        Open-source implementation of the AIFF format
License:        MIT
URL:            https://github.com/mtszb/libaiff
Source0:        libaiff-6.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Open-source implementation of the AIFF format

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
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0-1
- Initial openEuler RISC-V package from the full package inventory.
