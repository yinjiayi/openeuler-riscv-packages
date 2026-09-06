# SPDX-License-Identifier: Apache-2.0
Name:           yoga
Version:        3.2.1
Release:        2%{?dist}
Summary:        Cross-platform layout engine
License:        MIT
URL:            https://github.com/facebook/yoga
Source0:        yoga-3.2.1.tar.gz
Patch0:         0001-cmake-use-system-googletest.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make

%description
Cross-platform layout engine

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
%license LICENSE
%doc README.md

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.1-2
- Use the distribution GoogleTest package for the complete upstream test suite.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
