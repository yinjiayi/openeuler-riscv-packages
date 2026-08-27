# SPDX-License-Identifier: Apache-2.0
Name:           tpm2-totp
Version:        0.3.0
Release:        1%{?dist}
Summary:        Attest the trustworthiness of a device against a human using time-based one-time passwords
License:        BSD-3-Clause
URL:            https://github.com/tpm2-software/tpm2-totp
Source0:        tpm2-totp-0.3.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Attest the trustworthiness of a device against a human using time-based one-time passwords

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
