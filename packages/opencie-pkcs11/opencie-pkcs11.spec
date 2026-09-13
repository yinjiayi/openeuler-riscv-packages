# SPDX-License-Identifier: Apache-2.0
Name:           opencie-pkcs11
Version:        1.0.10
Release:        1%{?dist}
Summary:        Native PKCS#11 library for the Italian Electronic Identity Card (CIE)
License:        LGPL-3.0-or-later
URL:            https://github.com/M0Rf30/opencie-pkcs11
Source0:        opencie-pkcs11-1.0.10.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Native PKCS#11 library for the Italian Electronic Identity Card (CIE)

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.10-1
- Initial openEuler RISC-V package from the full package inventory.
