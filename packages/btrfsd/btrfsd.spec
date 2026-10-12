# SPDX-License-Identifier: Apache-2.0
Name:           btrfsd
Version:        0.2.2
Release:        1%{?dist}
Summary:        Tiny Btrfs maintenance daemon
License:        LGPL-2.1-or-later
URL:            https://github.com/ximion/btrfsd
Source0:        btrfsd-0.2.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Tiny Btrfs maintenance daemon

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
%doc NEWS.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
