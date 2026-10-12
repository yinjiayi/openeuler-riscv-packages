# SPDX-License-Identifier: Apache-2.0
Name:           cpp-kana
Version:        1.0.2
Release:        1%{?dist}
Summary:        A lightweight library for converting Japanese kana to romaji and vice versa.
License:        Apache-2.0
URL:            https://github.com/wolfgitpr/cpp-kana
Source0:        cpp-kana-1.0.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A lightweight library for converting Japanese kana to romaji and vice versa.

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
