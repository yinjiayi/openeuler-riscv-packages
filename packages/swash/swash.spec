# SPDX-License-Identifier: Apache-2.0
Name:           swash
Version:        1.5.1
Release:        3%{?dist}
Summary:        Fast screenshot annotator and lightweight image editor
License:        GPL-3.0-or-later
URL:            https://github.com/ItsLemmy/swash
Source0:        swash-1.5.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel

%description
Fast screenshot annotator and lightweight image editor

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-3
- Add the libadwaita development dependency required by Meson.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-2
- Add the GTK4 development dependency required by Meson.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-1
- Initial openEuler RISC-V package from the full package inventory.
