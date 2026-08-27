# SPDX-License-Identifier: Apache-2.0
Name:           milton
Version:        1.9.1
Release:        5%{?dist}
Summary:        An infinite-canvas paint program
License:        GPL-3.0-or-later
URL:            https://github.com/serge-rgb/milton
Source0:        milton-1.9.1.tar.gz
Patch0:         0001-keep-format-security-enabled.patch
Patch1:         0002-cmake-use-system-sdl2.patch
Patch2:         0003-guard-x86-intrinsics.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtk2-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  SDL2-devel

%description
An infinite-canvas paint program

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
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.1-5
- Include the unused SSE intrinsic headers only when compiling for x86.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.1-4
- Replace the bundled x86_64 SDL2 paths with the native system SDL2 package.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.1-3
- Add the SDL 2 development files required by the build.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.1-2
- Keep openEuler format-security compiler checks enabled.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.1-1
- Initial openEuler RISC-V package from the full package inventory.
