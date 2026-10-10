# SPDX-License-Identifier: Apache-2.0
Name:           ssdp-responder
Version:        2.0
Release:        1%{?dist}
Summary:        SSDP responder for Linux
License:        ISC
URL:            https://github.com/troglobit/ssdp-responder
Source0:        ssdp-responder-2.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
SSDP responder for Linux

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0-1
- Initial openEuler RISC-V package from the full package inventory.
