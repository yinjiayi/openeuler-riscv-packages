# SPDX-License-Identifier: Apache-2.0
Name:           gnome-rounded-blur
Version:        1.0.1
Release:        1%{?dist}
Summary:        GNOME Shell BlurEffect with rounded corners
License:        GPL-3.0-or-later
URL:            https://github.com/kancko/gnome-rounded-blur
Source0:        gnome-rounded-blur-1.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
GNOME Shell BlurEffect with rounded corners

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
