# SPDX-License-Identifier: Apache-2.0
Name:           yaml-cpp
Version:        0.9.0
Release:        1%{?dist}
Summary:        YAML parser and emitter for C++
License:        MIT
URL:            https://github.com/jbeder/yaml-cpp
Source0:        yaml-cpp-yaml-cpp-0.9.0.tar.gz

BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
yaml-cpp is a C++ library for parsing and emitting YAML documents.

%package devel
Summary:        Development files for yaml-cpp
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, linker name, CMake package configuration, and pkg-config metadata for
building applications with yaml-cpp.

%prep
%autosetup -c -n yaml-cpp-0.9.0

%build
cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_CXX_FLAGS_RELWITHDEBINFO='%{build_cxxflags}' \
  -DCMAKE_EXE_LINKER_FLAGS='%{build_ldflags}' \
  -DCMAKE_SHARED_LINKER_FLAGS='%{build_ldflags}' \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=%{_lib} \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DYAML_CPP_BUILD_TESTS=ON \
  -DYAML_CPP_BUILD_TOOLS=OFF \
  -DYAML_CPP_FORMAT_SOURCE=OFF \
  -DYAML_USE_SYSTEM_GTEST=OFF
cmake --build build --parallel %{?_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build

%check
ctest --test-dir build --output-on-failure

%files
%license LICENSE
%doc README.md
%{_libdir}/libyaml-cpp.so.*

%files devel
%{_includedir}/yaml-cpp/
%{_libdir}/libyaml-cpp.so
%{_libdir}/cmake/yaml-cpp/
%{_libdir}/pkgconfig/yaml-cpp.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.0-1
- Initial openEuler RISC-V package with the complete bundled CTest suite.
