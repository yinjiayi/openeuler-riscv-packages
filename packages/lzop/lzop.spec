# SPDX-License-Identifier: Apache-2.0
Name:           lzop
Version:        1.04
Release:        4%{?dist}
Summary:        Fast file compressor using the LZO library
License:        GPL-2.0-or-later
URL:            https://www.lzop.org/
Source0:        lzop-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  lzo-devel
BuildRequires:  make
BuildRequires:  pkgconf

%description
lzop is a file compressor designed for speed. It uses the LZO data compression
library and provides a gzip-like command-line interface.

%prep
%autosetup -p1

%build
%cmake_conf
%cmake_build

%install
%cmake_install

%check
%ctest -- -j1

%files
%license COPYING
%doc %{_docdir}/lzop/
%{_bindir}/lzop
%{_mandir}/man1/lzop.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.04-4
- Rebuild lzop for openEuler RISC-V from Fedora 44 and frozen cross-distribution evidence.
