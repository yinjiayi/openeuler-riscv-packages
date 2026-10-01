# SPDX-License-Identifier: Apache-2.0
Name:           gnome-console-jc
Version:        49.0
Release:        1%{?dist}
Summary:        A simple user-friendly terminal emulator for the GNOME desktop (JC fork)
License:        GPL-3.0-or-later
URL:            https://github.com/juancri/console
Source0:        gnome-console-jc-49.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A simple user-friendly terminal emulator for the GNOME desktop (JC fork)

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
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 49.0-1
- Initial openEuler RISC-V package from the full package inventory.
