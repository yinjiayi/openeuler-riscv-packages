# SPDX-License-Identifier: Apache-2.0
Name:           openssl-pkcs11-sign-provider
Version:        1.0.2
Release:        1%{?dist}
Summary:        OpenSSL Provider for asymmetric operations with private PKCS#11 keys
License:        Apache-2.0
URL:            https://github.com/opencryptoki/openssl-pkcs11-sign-provider
Source0:        openssl-pkcs11-sign-provider-1.0.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
OpenSSL Provider for asymmetric operations with private PKCS#11 keys

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
