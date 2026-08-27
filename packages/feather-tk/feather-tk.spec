# SPDX-License-Identifier: Apache-2.0
Name:           feather-tk
Version:        0.9.0
Release:        1%{?dist}
Summary:        A lightweight toolkit for building cross-platform applications
License:        BSD-3-Clause
URL:            https://github.com/grizzlypeak3d/feather-tk
Source0:        feather-tk-0.9.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A lightweight toolkit for building cross-platform applications

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
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.0-1
- Initial openEuler RISC-V package from the full package inventory.
