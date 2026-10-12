# SPDX-License-Identifier: Apache-2.0
Name:           feather-tk
Version:        0.9.0
Release:        2%{?dist}
Summary:        A lightweight toolkit for building cross-platform applications
License:        BSD-3-Clause
URL:            https://github.com/grizzlypeak3d/feather-tk
Source0:        feather-tk-0.9.0.tar.gz
Patch0:         0001-cmake-support-openEuler-3.27.patch
BuildRequires:  cmake >= 3.27
BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libpng-devel
BuildRequires:  lunasvg
BuildRequires:  make
BuildRequires:  mesa-dri-drivers
BuildRequires:  mesa-libGL-devel
BuildRequires:  nlohmann-json-devel
BuildRequires:  SDL2-devel
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  zlib-devel

%description
A lightweight toolkit for building cross-platform applications

%prep
%autosetup -p1

%build
%cmake \
  -Dftk_API=GL_4_1 \
  -Dftk_SDL2=ON \
  -Dftk_SDL3=OFF \
  -Dftk_nfd=OFF \
  -Dftk_PYTHON=OFF \
  -Dftk_TESTS=ON \
  -Dftk_EXAMPLES=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a \
  ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE.txt
%doc README.md

%changelog
* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.0-2
- Support the distribution CMake 3.27 toolchain.
- Declare the complete graphics, JSON, SVG, and Xvfb test dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.0-1
- Initial openEuler RISC-V package from the full package inventory.
