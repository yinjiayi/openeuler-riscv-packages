# SPDX-License-Identifier: Apache-2.0
Name:           cclip
Version:        3.3.1
Release:        1%{?dist}
Summary:        Clipboard manager for wayland
License:        GPL-3.0-or-later
URL:            https://github.com/heather7283/cclip
Source0:        cclip-3.3.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Clipboard manager for wayland

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
