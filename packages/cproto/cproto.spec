# SPDX-License-Identifier: Apache-2.0
Name:           cproto
Version:        4.8a
Release:        1%{?dist}
Summary:        C function prototype generator
License:        LicenseRef-Public-Domain AND MIT
URL:            https://invisible-island.net/cproto/
Source0:        cproto-4.8a.tgz

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gperf
BuildRequires:  make

%description
cproto generates C function prototypes and variable declarations from source
files, and can convert old-style function definitions to ANSI C syntax.

%prep
%autosetup -p1

%build
%configure --enable-llib
%make_build

%install
%make_install

%check
%make_build check

%files
%license LICENSE
%doc AUTHORS CHANGES README
%{_bindir}/cproto
%{_mandir}/man1/cproto.1*

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.8a-1
- Initial package from the official cproto 4.8a archive.
- Keep the complete upstream testing harness enabled in the networked target build.
