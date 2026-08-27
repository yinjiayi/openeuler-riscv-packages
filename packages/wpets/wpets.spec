# SPDX-License-Identifier: Apache-2.0
Name:           wpets
Version:        5.0.2
Release:        1%{?dist}
Summary:        A Wayland overlay that displays an animated virtual pet reacting to keyboard input
License:        MIT
URL:            https://github.com/furudbat/wayland-vpets
Source0:        wpets-5.0.2.tar.gz
Patch0:         patches/0001-riscv-drop-march-native.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  systemd-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel

%description
A Wayland overlay that displays an animated virtual pet reacting to keyboard input

%prep
%autosetup -n wayland-vpets-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
- Use the upstream archive's actual top-level directory.
- Add the Wayland, protocol, and libudev development files required by CMake.
- Leave RISC-V ISA selection to the distribution compiler flags.
