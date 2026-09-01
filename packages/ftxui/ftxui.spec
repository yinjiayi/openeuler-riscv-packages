# SPDX-License-Identifier: Apache-2.0
Name:           ftxui
Version:        7.0.3
Release:        1%{?dist}
Summary:        Functional terminal user interface library for C++
License:        MIT
URL:            https://github.com/ArthurSonzogni/FTXUI
Source0:        ftxui-7.0.3.tar.gz
Source1:        benchmark-1.8.2.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make
BuildRequires:  pkgconf

%description
FTXUI is a C++17 library for constructing functional terminal user
interfaces. It provides screen, document-object-model, and interactive
component libraries.

%package devel
Summary:        Development files for FTXUI
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Public C++ headers, unversioned linker names, pkg-config metadata, and CMake
package metadata for applications using FTXUI.

%prep
%autosetup -p1 -n FTXUI-%{version} -a 1

%build
cmake -S . -B build-shared \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING="%{build_cxxflags}" \
  -DCMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO:STRING="%{build_ldflags}" \
  -DCMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO:STRING="%{build_ldflags}" \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=%{_lib} \
  -DCMAKE_INSTALL_INCLUDEDIR=include \
  -DCMAKE_INSTALL_DATAROOTDIR=share \
  -DCMAKE_SKIP_RPATH=ON \
  -DBUILD_SHARED_LIBS=ON \
  -DFTXUI_BUILD_DOCS=OFF \
  -DFTXUI_BUILD_EXAMPLES=OFF \
  -DFTXUI_BUILD_MODULES=OFF \
  -DFTXUI_BUILD_TESTS=OFF \
  -DFTXUI_BUILD_TESTS_FUZZER=OFF \
  -DFTXUI_ENABLE_CCACHE=OFF \
  -DFTXUI_ENABLE_INSTALL=ON
%make_build -C build-shared

cmake -S . -B build-tests \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING="%{build_cxxflags}" \
  -DCMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO:STRING="%{build_ldflags}" \
  -DCMAKE_SKIP_RPATH=ON \
  -DBUILD_SHARED_LIBS=OFF \
  -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
  -DFETCHCONTENT_SOURCE_DIR_GOOGLEBENCHMARK="$PWD/benchmark-1.8.2" \
  -DFTXUI_BUILD_DOCS=OFF \
  -DFTXUI_BUILD_EXAMPLES=OFF \
  -DFTXUI_BUILD_MODULES=OFF \
  -DFTXUI_BUILD_TESTS=ON \
  -DFTXUI_BUILD_TESTS_FUZZER=OFF \
  -DFTXUI_ENABLE_CCACHE=OFF \
  -DFTXUI_ENABLE_INSTALL=OFF
%make_build -C build-tests

%install
DESTDIR=%{buildroot} cmake --install build-shared --config RelWithDebInfo

%check
test -x build-tests/ftxui-benchmark
ctest --test-dir build-tests \
  --output-on-failure --force-new-ctest-process -j1

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_libdir}/libftxui-component.so.7*
%{_libdir}/libftxui-dom.so.7*
%{_libdir}/libftxui-screen.so.7*

%files devel
%license LICENSE
%{_includedir}/ftxui/
%{_libdir}/libftxui-component.so
%{_libdir}/libftxui-dom.so
%{_libdir}/libftxui-screen.so
%{_libdir}/cmake/ftxui/
%{_libdir}/pkgconfig/ftxui.pc

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.0.3-1
- Initial openEuler RISC-V package with the complete registered test suite.
- Build the pinned upstream benchmark dependency without network access.
