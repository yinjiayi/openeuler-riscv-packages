# SPDX-License-Identifier: Apache-2.0
Name:           libgusb
Version:        0.4.9
Release:        1%{?dist}
Summary:        GObject wrapper for libusb1
License:        LGPL-2.1-or-later
URL:            https://github.com/hughsie/libgusb
Source0:        libgusb-0.4.9.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
GObject wrapper for libusb1

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.9-1
- Initial openEuler RISC-V package from the full package inventory.
