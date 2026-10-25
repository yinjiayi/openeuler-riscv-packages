# SPDX-License-Identifier: Apache-2.0
Name:           hestia
Version:        0.2.2
Release:        1%{?dist}
Summary:        hestia is a godness protect your root
License:        GPL-3.0-or-later
URL:            https://github.com/vbextreme/hestia
Source0:        hestia-0.2.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
hestia is a godness protect your root

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
