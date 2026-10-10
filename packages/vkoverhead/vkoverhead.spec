# SPDX-License-Identifier: Apache-2.0
Name:           vkoverhead
Version:        1.3
Release:        1%{?dist}
Summary:        Tool for evaluating CPU-based overhead of Vulkan drivers
License:        MIT
URL:            https://github.com/zmike/vkoverhead
Source0:        vkoverhead-1.3.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Tool for evaluating CPU-based overhead of Vulkan drivers

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3-1
- Initial openEuler RISC-V package from the full package inventory.
