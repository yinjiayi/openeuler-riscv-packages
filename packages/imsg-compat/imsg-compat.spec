# SPDX-License-Identifier: Apache-2.0
Name:           imsg-compat
Version:        8.0.0
Release:        1%{?dist}
Summary:        linux port of OpenBSD imsg utilities
License:        ISC
URL:            https://github.com/bsd-ac/imsg-compat
Source0:        imsg-compat-8.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
linux port of OpenBSD imsg utilities

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 8.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
