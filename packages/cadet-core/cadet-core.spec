# SPDX-License-Identifier: Apache-2.0
Name:           cadet-core
Version:        5.1.0
Release:        2%{?dist}
Summary:        Modeling and simulation framework for biotechnology processes – simulation backend
License:        AGPL-3.0 AND MPL-2.0
URL:            https://github.com/cadet/cadet-core
Source0:        cadet-core-5.1.0.tar.gz
Source1:        eigen-3.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Modeling and simulation framework for biotechnology processes – simulation backend

%prep
%autosetup -n CADET-Core-%{version} -p1 -a 1

%build
cmake -S eigen-3.4.0 -B eigen-build \
  -DCMAKE_INSTALL_PREFIX="$PWD/eigen-prefix" \
  -DBUILD_TESTING=OFF \
  -DEIGEN_BUILD_DOC=OFF
cmake --install eigen-build

%cmake -S . -B %{_vpath_builddir} \
  -DCMAKE_PREFIX_PATH="$PWD/eigen-prefix" \
  -DENABLE_TESTS=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE.txt
%doc README.rst

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.1.0-2
- Build against the pinned upstream Eigen 3.4.0 headers because the target
  repositories do not provide the required eigen3-devel version.
- Enable the upstream test suite through its actual ENABLE_TESTS option.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
