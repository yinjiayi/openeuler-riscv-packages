# SPDX-License-Identifier: Apache-2.0
%undefine _debugsource_packages

Name:           catch2
Version:        3.16.1
Release:        1%{?dist}
Summary:        Modern C++ test framework for unit tests, TDD, and BDD
License:        BSL-1.0
URL:            https://github.com/catchorg/Catch2
Source0:        v3.16.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3


%description
Catch2 is a modern C++ testing framework for unit tests, test-driven
development, and behavior-driven development.

%package devel
Summary:        Development files for Catch2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake integration, pkg-config metadata, and link libraries for Catch2.

%prep
%autosetup -p1 -n Catch2-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DCATCH_DEVELOPMENT_BUILD=ON \
  -DCATCH_ENABLE_WERROR=OFF \
  -DCATCH_INSTALL_DOCS=OFF \
  -DCATCH_INSTALL_EXTRAS=OFF
%cmake_build

%install
%cmake_install

%check
# Preserve runtime identity and generated test commands without running SelfTest
# outside the original suite. Diagnostics do not replace or filter the tests.
printf '%s\n' 'Catch2 default-suite diagnostics: CTest version and ELF digests'
ctest --version
ctest_executable="$(command -v ctest)"
sha256sum "$ctest_executable" "%{_vpath_builddir}/tests/SelfTest"
od -An -tx1 -N20 "$ctest_executable"
od -An -tx1 -N20 "%{_vpath_builddir}/tests/SelfTest"
printf '%s\n' 'Catch2 generated CTest registration (show-only; no tests executed)'
ctest --test-dir "%{_vpath_builddir}" --show-only=json-v1
# Run the full unfiltered suite in the CMake build tree; reject empty suites.
if ctest --test-dir "%{_vpath_builddir}" --no-tests=error \
  --verbose --output-on-failure --force-new-ctest-process -j1; then
  :
else
  ctest_status=$?
  printf '%s\n' 'Catch2 default suite failed; LastTest.log follows if available'
  if test -f "%{_vpath_builddir}/Testing/Temporary/LastTest.log"; then
    if cat "%{_vpath_builddir}/Testing/Temporary/LastTest.log"; then
      :
    else
      printf '%s\n' 'Could not read LastTest.log; preserving the CTest exit status'
    fi
  else
    printf '%s\n' 'LastTest.log is unavailable; preserving the CTest exit status'
  fi
  exit "$ctest_status"
fi

%files
%license LICENSE.txt
%doc README.md
%{_libdir}/libCatch2.so.3*
%{_libdir}/libCatch2Main.so.3*

%files devel
%license LICENSE.txt
%{_includedir}/catch2/
%{_libdir}/libCatch2.so
%{_libdir}/libCatch2Main.so
%{_libdir}/cmake/Catch2/
%{_datadir}/pkgconfig/catch2.pc
%{_datadir}/pkgconfig/catch2-with-main.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.15.3-1
- Initial openEuler RISC-V package.
- Run the complete CTest suite serially under QEMU.
