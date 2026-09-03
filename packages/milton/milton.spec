# SPDX-License-Identifier: Apache-2.0
Name:           milton
Version:        1.9.1
Release:        8%{?dist}
Summary:        An infinite-canvas paint program
License:        GPL-3.0-or-later
URL:            https://github.com/serge-rgb/milton
Source0:        milton-1.9.1.tar.gz
Patch0:         0001-keep-format-security-enabled.patch
Patch1:         0002-cmake-use-system-sdl2.patch
Patch2:         0003-guard-x86-intrinsics.patch
Patch3:         0004-fix-gcc14-cxx-errors.patch
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
install -Dpm0755 %{_vpath_builddir}/Milton %{buildroot}%{_bindir}/milton
# Milton resolves this bundled font relative to /proc/self/exe at runtime.
install -Dpm0644 %{_vpath_builddir}/Carlito.ttf %{buildroot}%{_bindir}/Carlito.ttf
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE.txt
%license third_party/Carlito.LICENSE
%doc README.md

%changelog
* Fri Aug 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.1-8
- Install the built executable and its runtime font explicitly.

* Fri Aug 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.1-7
- Keep C++ system headers outside C linkage and use explicit localized-text formats.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.1-6
- Regenerate the intrinsic-header patch with strict GNU patch context.

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
