# SPDX-License-Identifier: Apache-2.0
Name:           vipsdisp
Version:        4.1.4
Release:        1%{?dist}
Summary:        Tiny libvips / gtk+4 image viewer
License:        MIT
URL:            https://github.com/jcupitt/vipsdisp
Source0:        vipsdisp-4.1.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Tiny libvips / gtk+4 image viewer

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
%license LICENCE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.4-1
- Initial openEuler RISC-V package from the full package inventory.
