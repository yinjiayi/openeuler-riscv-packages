# SPDX-License-Identifier: Apache-2.0
Name:           clay
Version:        0.14
Release:        1%{?dist}
Summary:        Header-only high performance UI layout library in C
License:        Zlib
URL:            https://github.com/nicbarker/clay
Source0:        clay-0.14.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Header-only high performance UI layout library in C

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
%license LICENSE.md
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14-1
- Initial openEuler RISC-V package from the full package inventory.
