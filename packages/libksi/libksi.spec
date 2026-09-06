# SPDX-License-Identifier: Apache-2.0
Name:           libksi
Version:        3.21.3087
Release:        1%{?dist}
Summary:        GuardTime KSI API
License:        Apache-2.0
URL:            https://github.com/guardtime/libksi
Source0:        libksi-3.21.3087.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
GuardTime KSI API

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
%license license.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.21.3087-1
- Initial openEuler RISC-V package from the full package inventory.
