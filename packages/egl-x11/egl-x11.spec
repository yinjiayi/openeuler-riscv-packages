# SPDX-License-Identifier: Apache-2.0
Name:           egl-x11
Version:        1.0.5
Release:        1%{?dist}
Summary:        NVIDIA XLib and XCB EGL Platform Library
License:        Apache-2.0
URL:            https://github.com/NVIDIA/egl-x11
Source0:        egl-x11-1.0.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
NVIDIA XLib and XCB EGL Platform Library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.5-1
- Initial openEuler RISC-V package from the full package inventory.
