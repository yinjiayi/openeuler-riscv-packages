# SPDX-License-Identifier: Apache-2.0
Name:           tpm2-openssl
Version:        1.3.0
Release:        1%{?dist}
Summary:        OpenSSL Provider for Trusted Platform Module 2.0 integration
License:        BSD-3-Clause
URL:            https://github.com/tpm2-software/tpm2-openssl
Source0:        tpm2-openssl-1.3.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
OpenSSL Provider for Trusted Platform Module 2.0 integration

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
