# SPDX-License-Identifier: Apache-2.0
Name:           eastl
Version:        3.27.01
Release:        1%{?dist}
Summary:        Electronic Arts Standard Template Library. It is an extensive and robust implementation that has an emphasis on high performance.
License:        BSD-3-Clause
URL:            https://github.com/electronicarts/EASTL
Source0:        eastl-3.27.01.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Electronic Arts Standard Template Library. It is an extensive and robust implementation that has an emphasis on high performance.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.27.01-1
- Initial openEuler RISC-V package from the full package inventory.
