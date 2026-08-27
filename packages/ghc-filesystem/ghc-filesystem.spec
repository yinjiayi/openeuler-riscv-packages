# SPDX-License-Identifier: Apache-2.0
Name:           ghc-filesystem
Version:        1.5.16
Release:        1%{?dist}
Summary:        An implementation of C++17 std::filesystem for C++11 /C++14/C++17/C++20
License:        MIT
URL:            https://github.com/gulrak/filesystem
Source0:        ghc-filesystem-1.5.16.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
An implementation of C++17 std::filesystem for C++11 /C++14/C++17/C++20

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.16-1
- Initial openEuler RISC-V package from the full package inventory.
