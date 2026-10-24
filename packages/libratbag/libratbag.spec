# SPDX-License-Identifier: Apache-2.0
Name:           libratbag
Version:        0.18
Release:        1%{?dist}
Summary:        A DBus daemon to configure gaming mice
License:        MIT
URL:            https://github.com/libratbag/libratbag
Source0:        libratbag-0.18.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A DBus daemon to configure gaming mice

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.18-1
- Initial openEuler RISC-V package from the full package inventory.
