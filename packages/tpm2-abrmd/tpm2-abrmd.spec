# SPDX-License-Identifier: Apache-2.0
Name:           tpm2-abrmd
Version:        3.0.0
Release:        1%{?dist}
Summary:        Trusted Platform Module 2.0 Access Broker and Resource Management Daemon
License:        BSD-2-Clause
URL:            https://github.com/tpm2-software/tpm2-abrmd
Source0:        tpm2-abrmd-3.0.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Trusted Platform Module 2.0 Access Broker and Resource Management Daemon

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
