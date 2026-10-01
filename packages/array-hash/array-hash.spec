# SPDX-License-Identifier: Apache-2.0
Name:           array-hash
Version:        0.7.2
Release:        1%{?dist}
Summary:        C++ implementation of a fast and memory efficient hash map and hash set specialized for strings
License:        MIT
URL:            https://github.com/Tessil/array-hash
Source0:        array-hash-0.7.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ implementation of a fast and memory efficient hash map and hash set specialized for strings

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.2-1
- Initial openEuler RISC-V package from the full package inventory.
