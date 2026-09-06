# SPDX-License-Identifier: Apache-2.0
Name:           pins
Version:        2.4.6
Release:        1%{?dist}
Summary:        Create your own application shortcuts
License:        GPL-3.0-or-later
URL:            https://github.com/fabrialberio/Pins
Source0:        pins-2.4.6.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Create your own application shortcuts

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.6-1
- Initial openEuler RISC-V package from the full package inventory.
