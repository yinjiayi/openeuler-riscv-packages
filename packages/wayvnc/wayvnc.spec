# SPDX-License-Identifier: Apache-2.0
Name:           wayvnc
Version:        0.10.1
Release:        1%{?dist}
Summary:        VNC server for wlroots-based Wayland compositors
License:        ISC
URL:            https://github.com/any1/wayvnc
Source0:        wayvnc-0.10.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
VNC server for wlroots-based Wayland compositors

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10.1-1
- Initial openEuler RISC-V package from the full package inventory.
