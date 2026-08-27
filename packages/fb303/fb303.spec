# SPDX-License-Identifier: Apache-2.0
Name:           fb303
Version:        2025.10.27.00
Release:        1%{?dist}
Summary:        thrift functions that provide a mechanism for querying information from a service
License:        Apache-2.0
URL:            https://github.com/facebook/fb303
Source0:        fb303-2025.10.27.00.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
thrift functions that provide a mechanism for querying information from a service

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2025.10.27.00-1
- Initial openEuler RISC-V package from the full package inventory.
