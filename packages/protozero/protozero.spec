# SPDX-License-Identifier: Apache-2.0
Name:           protozero
Version:        1.8.2
Release:        1%{?dist}
Summary:        Minimalist protocol buffer decoder and encoder in C++
License:        BSD-2-Clause
URL:            https://github.com/mapbox/protozero
Source0:        protozero-1.8.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Minimalist protocol buffer decoder and encoder in C++

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
%license LICENSE.from_folly
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.2-1
- Initial openEuler RISC-V package from the full package inventory.
