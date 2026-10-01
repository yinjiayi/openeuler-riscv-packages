# SPDX-License-Identifier: Apache-2.0
Name:           libcgif
Version:        0.5.3
Release:        1%{?dist}
Summary:        A fast and lightweight GIF encoding library
License:        MIT
URL:            https://github.com/dloebl/cgif
Source0:        libcgif-0.5.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A fast and lightweight GIF encoding library

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.3-1
- Initial openEuler RISC-V package from the full package inventory.
