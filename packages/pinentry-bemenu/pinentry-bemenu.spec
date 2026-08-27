# SPDX-License-Identifier: Apache-2.0
Name:           pinentry-bemenu
Version:        0.14.0
Release:        1%{?dist}
Summary:        Pinentry based on bemenu
License:        GPL-3.0-or-later
URL:            https://github.com/t-8ch/pinentry-bemenu
Source0:        pinentry-bemenu-0.14.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Pinentry based on bemenu

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14.0-1
- Initial openEuler RISC-V package from the full package inventory.
