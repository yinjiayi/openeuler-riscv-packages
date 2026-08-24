# SPDX-License-Identifier: Apache-2.0
Name:           nasm
Version:        3.02
Release:        1%{?dist}
Summary:        Portable x86 assembler with Intel-like syntax
License:        BSD-2-Clause
URL:            https://www.nasm.us/
Source0:        nasm-%{version}.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  python3
BuildRequires:  zlib-devel

%description
NASM is a portable assembler for the x86 CPU architecture. It supports many
object formats and can run on non-x86 hosts to generate x86 machine code.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_build travis

%files
%license LICENSE
%doc AUTHORS CHANGES README.md
%{_bindir}/nasm
%{_bindir}/ndisasm
%{_mandir}/man1/nasm.1*
%{_mandir}/man1/ndisasm.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.02-1
- Initial openEuler RISC-V NASM package with complete upstream tests.
