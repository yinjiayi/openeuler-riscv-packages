# SPDX-License-Identifier: Apache-2.0
Name:           libv3270
Version:        5.5.0
Release:        1%{?dist}
Summary:        3270 Virtual Terminal for GTK
License:        LGPL-3.0-or-later
URL:            https://github.com/PerryWerneck/libv3270
Source0:        libv3270-5.5.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
3270 Virtual Terminal for GTK

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
%doc AUTHORS
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
