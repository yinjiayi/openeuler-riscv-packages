# SPDX-License-Identifier: Apache-2.0
Name:           ghostmirror
Version:        0.18.5
Release:        1%{?dist}
Summary:        modern alternative to reflector, true check mirror status, mirror download speed and more.
License:        GPL-3.0-or-later
URL:            https://github.com/vbextreme/ghostmirror
Source0:        ghostmirror-0.18.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
modern alternative to reflector, true check mirror status, mirror download speed and more.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.18.5-1
- Initial openEuler RISC-V package from the full package inventory.
