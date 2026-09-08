# SPDX-License-Identifier: Apache-2.0
Name:           intel-metrics-discovery
Version:        1.14.186
Release:        2%{?dist}
Summary:        User mode library providing access to Intel GPU performance data (MDAPI)
License:        MIT
URL:            https://github.com/intel/metrics-discovery
Source0:        intel-metrics-discovery-1.14.186.tar.gz
Patch0:         patches/0001-cmake-limit-x86-flags-to-x86.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libdrm-devel
BuildRequires:  make

%description
User mode library providing access to Intel GPU performance data (MDAPI)

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE.md
%doc README.md

%changelog
* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14.186-2
- Limit x86-only compiler and linker flags to x86 targets.
- Declare the libdrm development dependency required by upstream CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14.186-1
- Initial openEuler RISC-V package from the full package inventory.
