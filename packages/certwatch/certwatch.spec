# SPDX-License-Identifier: Apache-2.0
Name:           certwatch
Version:        1.2
Release:        1%{?dist}
Summary:        SSL/TLS certificate expiry warning generator
License:        GPL-2.0-or-later
URL:            https://github.com/notroj/certwatch
Source0:        certwatch-1.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
SSL/TLS certificate expiry warning generator

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
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2-1
- Initial openEuler RISC-V package from the full package inventory.
