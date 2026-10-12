# SPDX-License-Identifier: Apache-2.0
Name:           mawk
Epoch:          1
Version:        1.3.4.20260302
Release:        1%{?dist}
Summary:        Interpreter for the AWK programming language
License:        GPL-2.0-only
URL:            https://invisible-island.net/mawk/
Source0:        mawk-1.3.4-20260302.tgz

BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  sed

%description
mawk is an interpreter for the AWK pattern-scanning and text-processing
language, designed for efficient execution and POSIX-compatible behavior.

%prep
%autosetup -p1 -n mawk-1.3.4-20260302

%build
%configure
%make_build

%install
%make_install

%check
%{__make} check

%files
%license COPYING
%doc ACKNOWLEDGMENT CHANGES README
%{_bindir}/mawk
%{_mandir}/man1/mawk.1*
%{_mandir}/man7/mawk-arrays.7*
%{_mandir}/man7/mawk-code.7*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1:1.3.4.20260302-1
- Initial openEuler RISC-V package with all three upstream check targets.
