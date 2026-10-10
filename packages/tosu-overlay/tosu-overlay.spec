# SPDX-License-Identifier: Apache-2.0
Name:           tosu-overlay
Version:        2.1.1
Release:        1%{?dist}
Summary:        Overlay for osu! Powered by tosu, qt6, qt6-webengine and layer-shell-qt
License:        MIT
URL:            https://github.com/K4zoku/tosu-overlay-qt
Source0:        tosu-overlay-2.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Overlay for osu! Powered by tosu, qt6, qt6-webengine and layer-shell-qt

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
