# SPDX-License-Identifier: Apache-2.0
Name:           libxo
Version:        1.7.5
Release:        1%{?dist}
Summary:        A library for generating text, XML, JSON, and HTML output
License:        BSD-2-Clause
URL:            https://github.com/juniper/libxo
Source0:        libxo-1.7.5.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A library for generating text, XML, JSON, and HTML output

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
%license Copyright
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.5-1
- Initial openEuler RISC-V package from the full package inventory.
