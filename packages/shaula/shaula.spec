# SPDX-License-Identifier: Apache-2.0
Name:           shaula
Version:        0.1.8
Release:        4%{?dist}
Summary:        Capture, annotate, save, and copy screenshots on Wayland
License:        MIT
URL:            https://github.com/fgonzalezurriola/shaula
Source0:        shaula-0.1.8.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel
BuildRequires:  json-glib-devel

%description
Capture, annotate, save, and copy screenshots on Wayland

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.8-4
- Add the JSON-GLib development dependency required by Meson.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.8-3
- Add the GTK 4 development dependency required by Meson.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.8-2
- Add the GLib development dependency required by Meson.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.8-1
- Initial openEuler RISC-V package from the full package inventory.
