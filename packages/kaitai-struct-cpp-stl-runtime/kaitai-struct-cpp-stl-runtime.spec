# SPDX-License-Identifier: Apache-2.0
Name:           kaitai-struct-cpp-stl-runtime
Version:        0.11
Release:        1%{?dist}
Summary:        Kaitai Struct API for C++ using STL
License:        MIT
URL:            https://github.com/kaitai-io/kaitai_struct_cpp_stl_runtime
Source0:        kaitai-struct-cpp-stl-runtime-0.11.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Kaitai Struct API for C++ using STL

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Initial openEuler RISC-V package from the full package inventory.
