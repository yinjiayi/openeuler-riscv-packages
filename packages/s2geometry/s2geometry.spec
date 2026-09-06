# SPDX-License-Identifier: Apache-2.0
Name:           s2geometry
Version:        0.12.0
Release:        1%{?dist}
Summary:        A library for manipulating geometric shapes
License:        Apache-2.0
URL:            https://github.com/google/s2geometry
Source0:        s2geometry-0.12.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A library for manipulating geometric shapes

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12.0-1
- Initial openEuler RISC-V package from the full package inventory.
