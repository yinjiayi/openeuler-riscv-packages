# SPDX-License-Identifier: Apache-2.0
Name:           sniffercommit
Version:        0.3.3
Release:        1%{?dist}
Summary:        Fast C++20-powered pre-commit hook and CI generator
License:        MIT
URL:            https://github.com/slowy07/sniffercommit
Source0:        sniffercommit-0.3.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Fast C++20-powered pre-commit hook and CI generator

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-1
- Initial openEuler RISC-V package from the full package inventory.
