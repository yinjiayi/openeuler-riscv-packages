# SPDX-License-Identifier: Apache-2.0
Name:           cagebreak
Version:        3.2.1
Release:        1%{?dist}
Summary:        Tiling wayland compositor based on cage inspired by ratpoison
License:        MIT
URL:            https://github.com/project-repo/cagebreak
Source0:        cagebreak-3.2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Tiling wayland compositor based on cage inspired by ratpoison

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
