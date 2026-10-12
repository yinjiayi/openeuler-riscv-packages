# SPDX-License-Identifier: Apache-2.0
Name:           libzim-glib
Version:        4.0.0
Release:        1%{?dist}
Summary:        Partial GObject/C bindings for libzim
License:        GPL-3.0-or-later
URL:            https://github.com/birros/libzim-glib
Source0:        libzim-glib-4.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Partial GObject/C bindings for libzim

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
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
