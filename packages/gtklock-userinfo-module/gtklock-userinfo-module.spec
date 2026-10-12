# SPDX-License-Identifier: Apache-2.0
Name:           gtklock-userinfo-module
Version:        4.0.1
Release:        1%{?dist}
Summary:        gtklock module adding user info to the lockscreen
License:        GPL-3.0-or-later
URL:            https://github.com/jovanlanik/gtklock-userinfo-module
Source0:        gtklock-userinfo-module-4.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
gtklock module adding user info to the lockscreen

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
