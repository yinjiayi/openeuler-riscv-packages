# SPDX-License-Identifier: Apache-2.0
Name:           msdfgen
Version:        1.13
Release:        1%{?dist}
Summary:        Multi-channel signed distance field generator binary and library
License:        MIT
URL:            https://github.com/Chlumsky/msdfgen
Source0:        msdfgen-1.13.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Multi-channel signed distance field generator binary and library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.13-1
- Initial openEuler RISC-V package from the full package inventory.
