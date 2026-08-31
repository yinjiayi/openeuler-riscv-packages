# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           stuplot
Version:        1.0.0
Release:        4%{?dist}
Summary:        High-performance C++23 header-only plotting engine based on IA and DE
License:        MIT
URL:            https://github.com/Friendships6666/StuPlot
Source0:        stuplot-1.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
High-performance C++23 header-only plotting engine based on IA and DE

%prep
%autosetup -n StuPlot-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-4
- Disable the empty debuginfo subpackage for this header-only library.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-3
- Configure the explicit CMake source and out-of-source build directories.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-2
- Match the exact top-level directory in the official source archive.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
