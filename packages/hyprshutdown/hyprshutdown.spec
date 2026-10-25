# SPDX-License-Identifier: Apache-2.0
Name:           hyprshutdown
Version:        0.1.1
Release:        1%{?dist}
Summary:        A graceful shutdown utility for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprshutdown
Source0:        hyprshutdown-0.1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A graceful shutdown utility for Hyprland

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
