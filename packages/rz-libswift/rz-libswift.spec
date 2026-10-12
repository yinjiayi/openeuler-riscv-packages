# SPDX-License-Identifier: Apache-2.0
Name:           rz-libswift
Version:        0.8.0
Release:        1%{?dist}
Summary:        Swift Demangling library for Rizin
License:        Apache-2.0
URL:            https://github.com/rizinorg/rz-libswift
Source0:        rz-libswift-0.8.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Swift Demangling library for Rizin

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.0-1
- Initial openEuler RISC-V package from the full package inventory.
