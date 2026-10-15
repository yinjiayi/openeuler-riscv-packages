# SPDX-License-Identifier: Apache-2.0
# Installed payload is headers, CMake metadata and QA source, with no ELF files.
%global debug_package %{nil}

Name:           libcuckoo
Version:        0.3.1
Release:        1%{?dist}
Summary:        Header-only concurrent C++ hash table with C interface templates
License:        Apache-2.0 AND BSL-1.0
URL:            https://github.com/efficient/libcuckoo
Source0:        libcuckoo-0.3.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  rpm
BuildRequires:  gzip
BuildRequires:  tar
Requires:       gcc-c++
Requires:       cmake
Requires:       make
Requires:       bash
Requires:       coreutils
Requires:       rpm


%description
Header-only concurrent C++ hash table with C interface templates

%prep
%autosetup -n libcuckoo-ea8c36c65bf9cf83aaf6b0db971248c6ae3686cf -p1

%build
%set_build_flags
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="%{optflags} -UNDEBUG" \
  -DCMAKE_CXX_FLAGS="%{optflags} -UNDEBUG" \
  -DBUILD_EXAMPLES=ON -DBUILD_UNIT_TESTS=ON
cmake --build build --parallel %{_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/libcuckoo/qa/source
cp -a tests examples %{buildroot}%{_datadir}/libcuckoo/qa/source/
cat > %{buildroot}%{_datadir}/libcuckoo/qa/CMakeLists.txt <<'CMAKE'
# SPDX-License-Identifier: Apache-2.0
cmake_minimum_required(VERSION 3.1)
project(libcuckoo_installed_checks LANGUAGES C CXX)
find_package(libcuckoo 0.3.1 EXACT CONFIG REQUIRED PATHS /usr/share/cmake/libcuckoo NO_DEFAULT_PATH)
add_library(libcuckoo ALIAS libcuckoo::libcuckoo)
enable_testing()
# Original upstream tests/examples use installed headers, without source fallbacks.
add_subdirectory(source/tests/Catch catch)
add_subdirectory(source/tests/unit-tests unit-tests)
add_subdirectory(source/examples examples)
CMAKE

%check
ctest --test-dir build -N | grep -Fx 'Total Tests: 1'
ctest --test-dir build --output-on-failure --verbose

%files
%license LICENSE tests/Catch/LICENSE_1_0.txt
%doc README.md
%{_includedir}/libcuckoo/
%{_includedir}/libcuckoo-c/
%{_datadir}/cmake/libcuckoo/
%{_datadir}/libcuckoo/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.1-1
- Do not create an empty automatic debuginfo subpackage for a header-only payload.
- Package verified stable source, default install, original unit suite and examples.
