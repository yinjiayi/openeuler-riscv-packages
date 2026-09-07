# SPDX-License-Identifier: Apache-2.0
Name:           libigl
Version:        2.6.0
Release:        3%{?dist}
Summary:        Simple C++ geometry processing library
License:        GPL-3.0-or-later
URL:            https://github.com/libigl/libigl
Source0:        libigl-2.6.0.tar.gz
Patch0:         0001-use-system-eigen.patch
BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Simple C++ geometry processing library

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} \
  -DLIBIGL_BUILD_TESTS=OFF \
  -DLIBIGL_BUILD_TUTORIALS=OFF \
  -DLIBIGL_INSTALL=ON \
  -DLIBIGL_USE_STATIC_LIBRARY=OFF \
  -DLIBIGL_EMBREE=OFF \
  -DLIBIGL_GLFW=OFF \
  -DLIBIGL_IMGUI=OFF \
  -DLIBIGL_OPENGL=OFF \
  -DLIBIGL_STB=OFF \
  -DLIBIGL_PREDICATES=OFF \
  -DLIBIGL_SPECTRA=OFF \
  -DLIBIGL_XML=OFF \
  -DLIBIGL_COPYLEFT_CORE=OFF \
  -DLIBIGL_COPYLEFT_CGAL=OFF \
  -DLIBIGL_COPYLEFT_COMISO=OFF \
  -DLIBIGL_COPYLEFT_TETGEN=OFF \
  -DLIBIGL_RESTRICTED_MATLAB=OFF \
  -DLIBIGL_RESTRICTED_MOSEK=OFF \
  -DLIBIGL_RESTRICTED_TRIANGLE=OFF
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
printf '%s\n' \
  '#include <igl/adjacency_list.h>' \
  '#include <Eigen/Core>' \
  '#include <vector>' \
  'int main() {' \
  '  Eigen::MatrixXi faces(1, 3);' \
  '  faces << 0, 1, 2;' \
  '  std::vector<std::vector<int>> adjacency;' \
  '  igl::adjacency_list(faces, adjacency);' \
  '  return adjacency.size() == 3 ? 0 : 1;' \
  '}' > libigl-smoke.cpp
%{__cxx} %{optflags} -std=c++11 \
  -I%{buildroot}%{_includedir} -I%{_includedir}/eigen3 \
  libigl-smoke.cpp -o libigl-smoke
./libigl-smoke

%files -f %{name}.files
%license LICENSE.GPL
%license LICENSE.MPL2
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.0-3
- Accept the Eigen 3.3 compatibility series provided by openEuler 24.03.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.0-2
- Use system Eigen, disable unshipped optional modules, and compile-test core headers.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
