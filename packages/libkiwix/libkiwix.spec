# SPDX-License-Identifier: Apache-2.0
Name:           libkiwix
Version:        14.2.1
Release:        1%{?dist}
Summary:        Library providing the Kiwix software core
License:        GPL-3.0-or-later
URL:            https://github.com/kiwix/libkiwix
Source0:        libkiwix-14.2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Library providing the Kiwix software core

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
%license COPYING
%doc README.md
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 14.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
