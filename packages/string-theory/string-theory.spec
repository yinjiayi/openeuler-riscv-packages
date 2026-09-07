# SPDX-License-Identifier: Apache-2.0
Name:           string-theory
Version:        3.9
Release:        1%{?dist}
Summary:        Flexible UTF-8 string library and type-safe formatter for C++
License:        MIT
URL:            https://github.com/zrax/string_theory
Source0:        string-theory-3.9.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Flexible UTF-8 string library and type-safe formatter for C++

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.9-1
- Initial openEuler RISC-V package from the full package inventory.
