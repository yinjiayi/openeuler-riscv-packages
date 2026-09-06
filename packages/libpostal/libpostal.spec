# SPDX-License-Identifier: Apache-2.0
Name:           libpostal
Version:        1.1.4
Release:        1%{?dist}
Summary:        A C library for parsing/normalizing street addresses around the world
License:        MIT
URL:            https://github.com/openvenues/libpostal
Source0:        libpostal-1.1.4.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A C library for parsing/normalizing street addresses around the world

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
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.4-1
- Initial openEuler RISC-V package from the full package inventory.
