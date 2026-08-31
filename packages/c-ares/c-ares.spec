# SPDX-License-Identifier: Apache-2.0
Name:           c-ares
Version:        1.34.8
Release:        1%{?dist}
Summary:        Asynchronous DNS request library
License:        MIT
URL:            https://c-ares.org/
Source0:        c-ares-%{version}.tar.gz
Patch0:         0001-cmake-drop-redundant-gtest-system-include.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  make

%description
c-ares is a C library for asynchronous DNS requests, including a resolver
library and diagnostic command-line tools.

%package devel
Summary:        Development files for c-ares
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, manual pages, pkg-config metadata, CMake metadata, and the
unversioned library link for developing applications with c-ares.

%prep
%autosetup -p1

%build
# Upstream enables C++ only in the test subdirectory after its warning helper
# has created an empty normal-scope CMAKE_CXX_FLAGS.  Pass the RPM flags
# explicitly so openEuler's hardened PIE/PIC policy reaches the test objects.
%cmake_conf \
  -DCMAKE_CXX_FLAGS:STRING="%{optflags}" \
  -DCMAKE_NO_SYSTEM_FROM_IMPORTED=ON \
  -DCARES_BUILD_TESTS=ON \
  -DCARES_BUILD_TOOLS=ON \
  -DCARES_INSTALL=ON \
  -DCARES_SHARED=ON \
  -DCARES_STATIC=OFF \
  -DCARES_THREADS=ON
# Parallel RISC-V linker processes are unstable under QEMU user emulation and
# have been observed to terminate with SIGSEGV while linking the test tools.
# Keep the complete build, but run one link process at a time.
cmake --build %{_vpath_builddir} --verbose --parallel 1

%install
%cmake_install

%check
# Network is disabled during package builds. Keep every deterministic upstream
# unit/fuzz-corpus test while excluding only tests explicitly named Live*.
# Keep the test suite serial for the same QEMU process-stability constraint.
GTEST_FILTER='-*Live*' ctest --test-dir %{_vpath_builddir} \
  --output-on-failure --force-new-ctest-process -j1

%files
%license LICENSE.md
%doc AUTHORS README.md RELEASE-NOTES.md SECURITY.md
%{_bindir}/adig
%{_bindir}/ahost
%{_libdir}/libcares.so.2*
%{_mandir}/man1/adig.1*
%{_mandir}/man1/ahost.1*

%files devel
%license LICENSE.md
%{_includedir}/ares*.h
%{_libdir}/libcares.so
%{_libdir}/pkgconfig/libcares.pc
%{_libdir}/cmake/c-ares/
%{_mandir}/man3/ares*.3*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.34.8-1
- Initial openEuler RISC-V package with offline upstream tests.
- Serialize the QEMU-emulated build and test processes to avoid linker crashes.
- Preserve RPM C++ hardening flags for the late-enabled CMake test language.
