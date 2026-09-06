# SPDX-License-Identifier: Apache-2.0
Name:           libstorage-ng
Version:        4.5.341
Release:        1%{?dist}
Summary:        Library for storage management
License:        GPL-2.0-or-later
URL:            https://github.com/openSUSE/libstorage-ng
Source0:        libstorage-ng-4.5.341.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Library for storage management

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
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.5.341-1
- Initial openEuler RISC-V package from the full package inventory.
