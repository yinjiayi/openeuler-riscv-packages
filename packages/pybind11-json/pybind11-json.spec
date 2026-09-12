# SPDX-License-Identifier: Apache-2.0
Name:           pybind11-json
Version:        0.2.15
Release:        4%{?dist}
Summary:        Using nlohmann::json with pybind11
License:        BSD-3-Clause
URL:            https://github.com/pybind/pybind11_json
Source0:        pybind11-json-0.2.15.tar.gz
BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make
BuildRequires:  nlohmann-json3-devel
BuildRequires:  pybind11-devel
BuildRequires:  python3-devel
Requires:       nlohmann-json3-devel >= 3.2.0
Requires:       pybind11-devel >= 2.2.4

%description
Using nlohmann::json with pybind11

%prep
%autosetup -p1 -n pybind11_json-%{version}

%build
%cmake_conf -DBUILD_TESTS=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
test -x %{_vpath_builddir}/test/test_pybind11_json
%{_vpath_builddir}/test/test_pybind11_json

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Sun Sep 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.15-4
- Mark the installed header-only CMake package as noarch while retaining the
  architecture-native upstream test build and execution.

* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.15-3
- Use the openEuler out-of-source CMake configure macro expected by the build,
  install, and test helpers.

* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.15-2
- Match the official release archive's underscore-delimited source root.
- Declare all public and test dependencies and run the actual upstream suite.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.15-1
- Initial openEuler RISC-V package from the full package inventory.
