# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           simpleini
Version:        4.26
Release:        4%{?dist}
Summary:        Cross-platform C++ library providing a simple API to read and write INI-style configuration files
License:        MIT
URL:            https://github.com/brofield/simpleini
Source0:        simpleini-4.26.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make

%description
Cross-platform C++ library providing a simple API to read and write INI-style configuration files

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} \
  -DBUILD_TESTING=ON \
  -DSIMPLEINI_USE_SYSTEM_GTEST=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENCE.txt
%doc README.md

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.26-4
- Disable automatic debuginfo subpackages for this header-only library; the
  installed payload contains no compiled object from which to extract symbols.
- Preserve the complete upstream GoogleTest/CTest suite.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.26-3
- Raise the package timeout to 180 minutes after the complete dependency transaction
  exhausted the former 60-minute budget during downloads before rpmbuild began.
- Keep the full upstream CTest suite and library functionality enabled.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.26-2
- Build the upstream test suite against the matching system GoogleTest package.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.26-1
- Initial openEuler RISC-V package from the full package inventory.
