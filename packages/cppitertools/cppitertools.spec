# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           cppitertools
Version:        2.2
Release:        2%{?dist}
Summary:        Python itertools and builtin iteration functions for C++17
License:        BSD-2-Clause
URL:            https://github.com/ryanhaining/cppitertools
Source0:        cppitertools-2.2.tar.gz
Source1:        catch-2.13.10.hpp
BuildArch:      noarch
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Python itertools and builtin iteration functions for C++17

%prep
%autosetup -p1
install -pm 0644 %{SOURCE1} test/catch.hpp

%build
%cmake_conf
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
cmake -S test -B %{_vpath_builddir}/tests \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING="%{build_cxxflags}" \
  -DCMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO:STRING="%{build_ldflags}"
cmake --build %{_vpath_builddir}/tests --parallel 2
# Upstream does not register CTest cases. This aggregate Catch2 binary contains
# the complete test source set discovered by test/CMakeLists.txt.
%{_vpath_builddir}/tests/test_all

%files -f %{name}.files
%license LICENSE.md
%doc README.md

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2-2
- Use the repository's separate CMake build directory contract.
- Build and execute the complete upstream test aggregate with pinned Catch2.
- Mark the header-only result noarch and suppress an empty debuginfo package.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2-1
- Initial openEuler RISC-V package from the full package inventory.
