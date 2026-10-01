# SPDX-License-Identifier: Apache-2.0
Name:           yabridge
Version:        5.1.1
Release:        1%{?dist}
Summary:        A modern and transparent way to use Windows VST2 and VST3 plugins on Linux
License:        GPL-3.0-or-later
URL:            https://github.com/robbert-vdh/yabridge
Source0:        yabridge-5.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A modern and transparent way to use Windows VST2 and VST3 plugins on Linux

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
