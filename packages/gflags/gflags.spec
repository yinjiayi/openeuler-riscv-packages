# SPDX-License-Identifier: Apache-2.0
Name:           gflags
Version:        2.3.1
Release:        1%{?dist}
Summary:        C++ library for command-line flag processing
License:        BSD-3-Clause
URL:            https://gflags.github.io/gflags/
Source0:        v2.3.1.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3

%description
gflags is a C++ library that implements command-line flags with support for
distributed declaration and definition across source files.

%package devel
Summary:        Development files for gflags
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, static libraries, unversioned shared-library links, pkg-config data,
and CMake package metadata for developing applications with gflags.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DGFLAGS_LIBRARY_INSTALL_DIR=%{_lib} \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=ON \
  -DBUILD_gflags_LIB=ON \
  -DBUILD_gflags_nothreads_LIB=ON \
  -DBUILD_TESTING=ON \
  -DBUILD_NC_TESTS=ON \
  -DBUILD_CONFIG_TESTS=ON \
  -DINSTALL_HEADERS=ON \
  -DINSTALL_SHARED_LIBS=ON \
  -DINSTALL_STATIC_LIBS=ON \
  -DREGISTER_BUILD_DIR=OFF \
  -DREGISTER_INSTALL_PREFIX=OFF
%cmake_build

%install
%cmake_install

%check
# gflags 2.2.2's configuration consumer links gflags::gflags, while its
# generated config intentionally requires an opt-in for namespaced targets.
# Limit that documented opt-in to the configuration consumer so the separate
# negative-compilation projects continue to exercise non-namespaced targets.
namespace_init="$PWD/gflags-config-test-init.cmake"
cat >"$namespace_init" <<'CMAKE'
if (TEST_NAME STREQUAL "cmake_config")
  set(GFLAGS_USE_TARGET_NAMESPACE ON CACHE BOOL
      "Use namespaced targets in the package configuration consumer" FORCE)
endif ()
CMAKE
ctest_log="$PWD/gflags-ctest.log"
CMAKE_TOOLCHAIN_FILE="$namespace_init" \
  ctest --test-dir %{_vpath_builddir} \
    --output-on-failure --force-new-ctest-process -j1 \
    >"$ctest_log" 2>&1
cat "$ctest_log"

%files
%license COPYING.txt
%doc AUTHORS.txt ChangeLog.txt README.md
%{_bindir}/gflags_completions.sh
%{_libdir}/libgflags.so.2.3*
%{_libdir}/libgflags_nothreads.so.2.3*

%files devel
%license COPYING.txt
%{_includedir}/gflags/
%{_libdir}/libgflags.a
%{_libdir}/libgflags.so
%{_libdir}/libgflags_nothreads.a
%{_libdir}/libgflags_nothreads.so
%{_libdir}/cmake/gflags/
%{_libdir}/pkgconfig/gflags.pc

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.2-1
- Initial openEuler RISC-V package with all 57 upstream CTest cases enabled.
