# SPDX-License-Identifier: Apache-2.0
Name:           wl-clipboard
Version:        2.3.0
Release:        1%{?dist}
Summary:        Command-line copy/paste utilities for Wayland
License:        GPL-3.0-or-later
URL:            https://github.com/bugaevc/wl-clipboard
Source0:        wl-clipboard-2.3.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Command-line copy/paste utilities for Wayland

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
