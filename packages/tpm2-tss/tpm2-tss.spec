# SPDX-License-Identifier: Apache-2.0
Name:           tpm2-tss
Version:        4.1.3
Release:        5%{?dist}
Summary:        Implementation of the TCG Trusted Platform Module 2.0 Software Stack (TSS2)
License:        BSD-2-Clause
URL:            https://github.com/tpm2-software/tpm2-tss
Source0:        tpm2-tss-4.1.3.tar.gz
BuildRequires:  gcc
BuildRequires:  json-c-devel
BuildRequires:  libcmocka-devel
BuildRequires:  libcurl-devel
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  util-linux-devel

%description
Implementation of the TCG Trusted Platform Module 2.0 Software Stack (TSS2)

%prep
%autosetup -p1

%build
%configure --enable-unit
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) \
    ! -path '%{buildroot}%{_mandir}/*' \
    -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.3-5
- Keep compressed manual pages out of the pre-compression generated file manifest.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.3-4
- Add the OpenSSL command-line tool required to generate unit-test fixtures.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.3-3
- Build from the official GNU-style release tarball with its generated configure files.
- Pin the independently recomputed release-asset SHA-256.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.3-2
- Declare the Autoconf macros and core crypto, JSON, HTTP, and UUID providers.
- Enable the upstream cmocka unit tests while leaving integration tests disabled.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.3-1
- Initial openEuler RISC-V package from the full package inventory.
