# SPDX-License-Identifier: Apache-2.0
Name:           qatzip
Version:        1.3.2
Release:        1%{?dist}
Summary:        Intel QuickAssist Technology (QAT) QATzip Library
License:        BSD-3-Clause
URL:            https://github.com/intel/QATzip
Source0:        qatzip-1.3.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Intel QuickAssist Technology (QAT) QATzip Library

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
%license LICENSE.LZ4
%license LICENSE.XXHASH
%license LICENSE.ZLIB
%license LICENSE.ZSTD
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
