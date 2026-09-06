# SPDX-License-Identifier: Apache-2.0
Name:           mgard
Version:        1.6.0
Release:        1%{?dist}
Summary:        MultiGrid Adaptive Reduction of Data
License:        Apache-2.0
URL:            https://github.com/CODARcode/MGARD
Source0:        mgard-1.6.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
MultiGrid Adaptive Reduction of Data

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
%license Copyright.txt
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
