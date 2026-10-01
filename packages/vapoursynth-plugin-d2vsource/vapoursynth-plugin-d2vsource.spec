# SPDX-License-Identifier: Apache-2.0
Name:           vapoursynth-plugin-d2vsource
Version:        1.4
Release:        1%{?dist}
Summary:        Plugin for Vapoursynth: d2vsource
License:        LGPL-2.1-or-later
URL:            https://github.com/dwbuiten/d2vsource
Source0:        vapoursynth-plugin-d2vsource-1.4.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Plugin for Vapoursynth: d2vsource

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4-1
- Initial openEuler RISC-V package from the full package inventory.
