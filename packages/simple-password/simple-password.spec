# SPDX-License-Identifier: Apache-2.0
Name:           simple-password
Version:        0.1.1
Release:        7%{?dist}
Summary:        A password generator without any unnecessary stuff
License:        GPL-3.0-or-later
URL:            https://github.com/ESzPa/spass
Source0:        simple-password-0.1.1.tar.gz
Patch0:         0001-tests-add-generation-unit-coverage.patch
BuildRequires:  argparse
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  vim-common

%description
A password generator without any unnecessary stuff

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
test_count="$(ctest --test-dir %{_vpath_builddir} -N | awk '/^Total Tests:/ { print $3 }')"
test "${test_count:-0}" -gt 0
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE


%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-7
- Correct the downstream test patch hunk length so the test program retains
  its return statement and closing brace.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-6
- Add deterministic unit coverage for the generation primitives and fail the
  package build when CTest registers no tests.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-5
- Raise the package timeout to 180 minutes after both exact-head CI attempts
  exhausted the former 60-minute budget during dependency downloads.
- Keep the complete upstream test and command-line functionality enabled.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-4
- Add the argparse header provider required by the command-line interface.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-3
- Configure the explicit CMake source and out-of-source build directories.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-2
- Add the vim-common provider for the xxd source-generation command.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
