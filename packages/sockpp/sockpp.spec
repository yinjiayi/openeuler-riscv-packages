# SPDX-License-Identifier: Apache-2.0
Name:           sockpp
Version:        1.0.0
Release:        3%{?dist}
Summary:        Simple, modern, C++ socket library.
License:        BSD-3-Clause
URL:            https://github.com/fpagliughi/sockpp
Source0:        sockpp-1.0.0.tar.gz
BuildRequires:  catch2-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Simple, modern, C++ socket library.

%prep
%autosetup -p1

%build
%cmake -DSOCKPP_BUILD_TESTS=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-3
- Raise the package timeout to 180 minutes after the complete dependency transaction
  exhausted the former 60-minute budget during downloads before rpmbuild began.
- Keep the full upstream Catch2 test suite and library functionality enabled.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-2
- Enable the upstream Catch2 unit tests with the project's actual CMake option.
- Add the Catch2 development files required to configure and build the tests.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
