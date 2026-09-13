# SPDX-License-Identifier: Apache-2.0
Name:           doctest
Version:        2.5.3
Release:        1%{?dist}
Summary:        Lightweight feature-rich C++ testing framework
License:        MIT AND CC-BY-4.0 AND BSL-1.0 AND BSD-3-Clause
URL:            https://github.com/doctest/doctest
Source0:        doctest-2.5.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

# doctest installs headers, CMake/pkg-config metadata, and a static archive.
# The target RPM macros otherwise create an empty debuginfo file list and fail
# packaging after the complete upstream test suite has passed.
%global debug_package %{nil}


%description
doctest is a lightweight, feature-rich C++ testing framework.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DDOCTEST_WITH_TESTS=ON \
  -DDOCTEST_WITH_MAIN_IN_STATIC_LIB=ON
%cmake_build

%install
%cmake_install
install -Dpm 0644 %{_vpath_builddir}/libdoctest_with_main.a \
  %{buildroot}%{_libdir}/libdoctest_with_main.a

%check
# QEMU user mode has produced process-level SIGILL at varying points in otherwise
# successful runs.  Keep the full upstream suite, but bound each ctest process
# to eight tests so emulator state is renewed more frequently.
test_count=$(ctest --test-dir %{_vpath_builddir} -N | \
  sed -n 's/^Total Tests: //p')
test "$test_count" -gt 0
first=1
while test "$first" -le "$test_count"; do
  last=$((first + 7))
  test "$last" -le "$test_count" || last=$test_count
  ctest --test-dir %{_vpath_builddir} \
    --output-on-failure --force-new-ctest-process -j1 \
    -I "$first,$last"
  first=$((last + 1))
done

%files
%license LICENSE.txt
%doc README.md
%{_includedir}/doctest/
%{_libdir}/libdoctest_with_main.a
%{_libdir}/cmake/doctest/
%{_libdir}/pkgconfig/doctest.pc

%changelog
* Sun Sep 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.3-1
- Update to the verified official stable 2.5.3 archive.
- Retain the complete dynamic CTest batches and disable empty debuginfo output.

* Wed Sep 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.2-4
- Disable the empty debuginfo subpackage for the header/static-only payload.

* Wed Sep 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.2-3
- Use shorter CTest batches after a 32-test batch still accumulated QEMU state.

* Wed Sep 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.2-2
- Run the complete CTest suite in bounded batches under QEMU user mode.

* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.2-1
- Initial openEuler RISC-V package.
- Run the complete CTest suite serially under QEMU.
