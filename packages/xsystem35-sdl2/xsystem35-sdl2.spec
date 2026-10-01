# SPDX-License-Identifier: Apache-2.0
Name:           xsystem35-sdl2
Version:        2.19.0
Release:        3%{?dist}
Summary:        This is a multi-platform port of xsystem35, a free implementation of AliceSoft's System 3.x game engine.
License:        GPL-2.0-or-later
URL:            https://github.com/kichikuou/xsystem35-sdl2
Source0:        xsystem35-sdl2-2.19.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  SDL2-devel
BuildRequires:  zlib-devel

%description
This is a multi-platform port of xsystem35, a free implementation of AliceSoft's System 3.x game engine.

%prep
%autosetup -p1

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
%license COPYING
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.19.0-3
- Add the SDL 2 development dependency required by pkg-config.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.19.0-2
- Add the Zlib development dependency required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.19.0-1
- Initial openEuler RISC-V package from the full package inventory.
