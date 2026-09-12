# SPDX-License-Identifier: Apache-2.0
Name:           sniffercommit
Version:        0.3.3
Release:        5%{?dist}
Summary:        Fast C++20-powered pre-commit hook and CI generator
License:        MIT AND BSD-3-Clause
URL:            https://github.com/slowy07/sniffercommit
Source0:        sniffercommit-0.3.3.tar.gz
Source1:        fmt-11.0.2.tar.gz
Source2:        tomlplusplus-3.4.0.tar.gz
Source3:        googletest-1.15.2.tar.gz
BuildRequires:  cmake
BuildRequires:  clang-tools-extra
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  make

%description
Fast C++20-powered pre-commit hook and CI generator

%prep
%autosetup -n metis-%{version} -p1 -a 1 -a 2 -a 3
cp -p fmt-11.0.2/LICENSE LICENSE.fmt
cp -p tomlplusplus-3.4.0/LICENSE LICENSE.tomlplusplus
cp -p googletest-1.15.2/LICENSE LICENSE.googletest

%build
%cmake -S . -B %{_vpath_builddir} \
  -DSNIFFERCOMMIT_BUILD_TESTS=ON \
  -DBUILD_SHARED_LIBS=OFF \
  -DFMT_INSTALL=OFF \
  -DINSTALL_GTEST=OFF \
  -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
  -DFETCHCONTENT_SOURCE_DIR_FMT="$PWD/fmt-11.0.2" \
  -DFETCHCONTENT_SOURCE_DIR_TOMLPLUSPLUS="$PWD/tomlplusplus-3.4.0" \
  -DFETCHCONTENT_SOURCE_DIR_GOOGLETEST="$PWD/googletest-1.15.2"
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%license LICENSE.fmt LICENSE.tomlplusplus LICENSE.googletest
%doc README.md

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-5
- Pin all FetchContent sources and bind configuration to verified local archives.
- Keep dependency libraries private and static without third-party install exports.
- Retain the full upstream test suite and include dependency license notices.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-4
- Add the official clang-format provider required by the complete test suite.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-3
- Configure explicitly out of source in the shared RPM CMake build directory.
- Keep build, install, and the full upstream CTest suite on that same directory.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-2
- Match the renamed upstream archive root and declare FetchContent's git dependency.
- Enable the upstream CTest suite through its actual CMake option.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-1
- Initial openEuler RISC-V package from the full package inventory.
