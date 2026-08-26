# SPDX-License-Identifier: Apache-2.0
Name:           tpm2-tss
Version:        4.1.3
Release:        1%{?dist}
Summary:        Implementation of the TCG Trusted Platform Module 2.0 Software Stack (TSS2)
License:        BSD-2-Clause
URL:            https://github.com/tpm2-software/tpm2-tss
Source0:        tpm2-tss-4.1.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Implementation of the TCG Trusted Platform Module 2.0 Software Stack (TSS2)

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.3-1
- Initial openEuler RISC-V package from the full package inventory.
