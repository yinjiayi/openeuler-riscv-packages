# SPDX-License-Identifier: Apache-2.0
Name:           pipexec
Version:        2.6.2
Release:        1%{?dist}
Summary:        Connector of arbitrary file descriptors
License:        GPL-2.0-or-later
URL:            https://github.com/flonatel/pipexec
Source0:        pipexec-2.6.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Connector of arbitrary file descriptors

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.2-1
- Initial openEuler RISC-V package from the full package inventory.
