# SPDX-License-Identifier: Apache-2.0
Name:           libjcat
Version:        0.2.6
Release:        1%{?dist}
Summary:        Library for reading and writing Jcat files
License:        LGPL-2.1-or-later
URL:            https://github.com/hughsie/libjcat
Source0:        libjcat-0.2.6.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Library for reading and writing Jcat files

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.6-1
- Initial openEuler RISC-V package from the full package inventory.
