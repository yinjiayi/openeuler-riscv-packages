# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           vatomic
Version:        2.4.1
Release:        9%{?dist}
Summary:        VSync atomics - formally-verified atomic operations library
License:        MIT
URL:            https://github.com/open-s4c/vatomic
Source0:        vatomic-2.4.1.tar.gz
Patch0:         0001-tests-use-valid-std-atomic-memory-orders.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libatomic
BuildRequires:  make

%description
VSync atomics - formally-verified atomic operations library

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} \
  -DVATOMIC_DEV=OFF \
  -DVATOMIC_TESTS=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) \
  ! -path '%{buildroot}%{_mandir}/*' \
  -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md
%{_mandir}/man3/vatomic_*.3*
%{_mandir}/man7/vatomic.7*

%changelog
* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-9
- Disable the empty debuginfo subpackage for this header-only library.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-8
- Package manual pages with compression-compatible globs outside the generated file list.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-7
- Use valid compare-exchange failure memory orders in the C++ comparison tests.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-6
- Correct the first patch hunk boundary for strict GNU patch application.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-5
- Use only valid C++ memory orders in the upstream atomic comparison tests.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-4
- Require the RISC-V libatomic runtime used by the upstream test suite.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-3
- Configure CMake in the build directory consumed by the RPM macros.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-2
- Use the upstream test options and add the C++ compiler required by the test suite.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
