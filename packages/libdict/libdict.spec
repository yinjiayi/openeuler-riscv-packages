# SPDX-License-Identifier: Apache-2.0
Name:           libdict
Version:        1.0.3
Release:        1%{?dist}
Summary:        C library of key-value data structures with an object-oriented interface
License:        BSD-2-Clause
URL:            https://github.com/rtbrick/libdict
Source0:        libdict-1.0.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
C library of key-value data structures with an object-oriented interface

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
