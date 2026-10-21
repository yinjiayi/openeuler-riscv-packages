# SPDX-License-Identifier: Apache-2.0
Name:           uncrustify
Version:        0.83.0
Release:        1%{?dist}
Summary:        Source-code beautifier for many programming languages
License:        GPL-2.0-only
URL:            https://github.com/uncrustify/uncrustify
Source0:        uncrustify-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3

%description
Uncrustify is a configurable source-code formatter supporting C, C++, C#,
Objective-C, Java, D, Pawn, Vala, ECMAScript, and related languages.

%prep
%autosetup -p1 -n uncrustify-uncrustify-%{version}

%build
%cmake_conf -DBUILD_TESTING=ON -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING
%{_bindir}/uncrustify
%{_mandir}/man1/uncrustify.1*
%{_docdir}/uncrustify/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.83.0-1
- Initial openEuler RISC-V package with the complete 14-entry Release test gate.
