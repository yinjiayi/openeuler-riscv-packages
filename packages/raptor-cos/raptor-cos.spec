# SPDX-License-Identifier: Apache-2.0
Name:           raptor-cos
Version:        0.8.1
Release:        6%{?dist}
Summary:        Vertically-scrolling shoot 'em up from 1994
License:        GPL-2.0-or-later
URL:            https://github.com/skynettx/raptor
Source0:        raptor-cos-0.8.1.tar.gz
Patch0:         0001-cmake-fallback-to-pkg-config-for-sdl2.patch
Patch1:         0002-cmake-use-pkg-config-for-alsa.patch
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(sdl2)

%description
Vertically-scrolling shoot 'em up from 1994

%prep
%autosetup -n raptor-%{version} -N
sed -i 's/\r$//' CMakeLists.txt
%autopatch -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON -DCMAKE_POSITION_INDEPENDENT_CODE=ON
%cmake_build

%install
install -Dpm 0755 %{_vpath_builddir}/bin/raptor %{buildroot}%{_bindir}/raptor
install -Dpm 0755 %{_vpath_builddir}/bin/raptorsetup %{buildroot}%{_bindir}/raptorsetup
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-6
- Supply SDL2 imported targets when CMake's legacy finder returns variables only.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-5
- Load CMake's PkgConfig module before resolving the official ALSA metadata.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-4
- Compile all bundled static objects as PIC before linking the hardened executable.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-3
- Use the official ALSA pkg-config metadata when CMake cannot infer lib64.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-2
- Fall back to the official SDL2 pkg-config metadata on Linux.
- Install both executables explicitly because upstream has no install rule.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-1
- Initial openEuler RISC-V package from the full package inventory.
