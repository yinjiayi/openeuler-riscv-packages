# SPDX-License-Identifier: Apache-2.0
Name:           sniffercommit
Version:        0.3.3
Release:        4%{?dist}
Summary:        Fast C++20-powered pre-commit hook and CI generator
License:        MIT
URL:            https://github.com/slowy07/sniffercommit
Source0:        sniffercommit-0.3.3.tar.gz
BuildRequires:  cmake
BuildRequires:  clang-tools-extra
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  make

%description
Fast C++20-powered pre-commit hook and CI generator

%prep
%autosetup -n metis-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} \
  -DSNIFFERCOMMIT_BUILD_TESTS=ON
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
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-4
- Add the official clang-format provider required by the complete test suite.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-3
- Configure explicitly out of source in the shared RPM CMake build directory.
- Keep build, install, and the full upstream CTest suite on that same directory.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-2
- Match the renamed upstream archive root and declare FetchContent's git dependency.
- Enable the upstream CTest suite through its actual CMake option.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-1
- Initial openEuler RISC-V package from the full package inventory.
