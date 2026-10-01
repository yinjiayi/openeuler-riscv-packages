# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           semver-cpp
Version:        1.0.0
Release:        3%{?dist}
Summary:        Semantic versioning for modern C++.
License:        MIT
URL:            https://github.com/Neargye/semver
Source0:        semver-cpp-1.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Semantic versioning for modern C++.

%prep
%autosetup -n semver-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} -DSEMVER_OPT_BUILD_TESTS=ON
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
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-3
- Disable the automatic debuginfo subpackage for the header-only payload.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-2
- Use the verified upstream archive root during source preparation.
- Configure the explicit CMake build directory and enable the bundled doctest suite.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
