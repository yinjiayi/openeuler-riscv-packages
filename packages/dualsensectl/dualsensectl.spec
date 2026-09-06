# SPDX-License-Identifier: Apache-2.0
Name:           dualsensectl
Version:        0.7
Release:        1%{?dist}
Summary:        Linux tool for controlling PS5 DualSense controller
License:        GPL-2.0-or-later
URL:            https://github.com/nowrep/dualsensectl
Source0:        dualsensectl-0.7.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Linux tool for controlling PS5 DualSense controller

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7-1
- Initial openEuler RISC-V package from the full package inventory.
