# SPDX-License-Identifier: Apache-2.0
Name:           rog-daemon
Version:        2.1.0
Release:        1%{?dist}
Summary:        Lightweight daemon and CLI to control ASUS ROG/TUF laptops features
License:        GPL-3.0-or-later
URL:            https://github.com/mechakotik/rog-daemon
Source0:        rog-daemon-2.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Lightweight daemon and CLI to control ASUS ROG/TUF laptops features

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
