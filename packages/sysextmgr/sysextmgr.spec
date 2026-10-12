# SPDX-License-Identifier: Apache-2.0
Name:           sysextmgr
Version:        1.0.0
Release:        1%{?dist}
Summary:        Tools to manage systemd-sysext images
License:        GPL-2.0-or-later
URL:            https://github.com/thkukuk/sysextmgr
Source0:        sysextmgr-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Tools to manage systemd-sysext images

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
%license LICENSE.GPL2
%license LICENSE.LGPL2.1
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
