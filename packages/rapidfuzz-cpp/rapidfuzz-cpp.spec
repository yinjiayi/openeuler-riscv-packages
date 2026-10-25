# SPDX-License-Identifier: Apache-2.0
Name:           rapidfuzz-cpp
Version:        3.3.3
Release:        1%{?dist}
Summary:        Rapid fuzzy string matching in C++ using the Levenshtein Distance
License:        MIT
URL:            https://github.com/rapidfuzz/rapidfuzz-cpp
Source0:        rapidfuzz-cpp-3.3.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Rapid fuzzy string matching in C++ using the Levenshtein Distance

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.3-1
- Initial openEuler RISC-V package from the full package inventory.
