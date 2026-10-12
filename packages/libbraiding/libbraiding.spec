# SPDX-License-Identifier: Apache-2.0
Name:           libbraiding
Version:        1.3.2
Release:        1%{?dist}
Summary:        Library to compute several properties of braids, including centralizer and conjugacy check
License:        GPL-3.0-or-later
URL:            https://github.com/enriqueartal/libbraiding
Source0:        libbraiding-1.3.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Library to compute several properties of braids, including centralizer and conjugacy check

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
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
