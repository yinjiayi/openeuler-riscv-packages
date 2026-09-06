# SPDX-License-Identifier: Apache-2.0
Name:           libwdm
Version:        0.2.6
Release:        1%{?dist}
Summary:        Header-only C++ library for weighted dependence measures
License:        MIT
URL:            https://github.com/tnagler/wdm
Source0:        libwdm-0.2.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Header-only C++ library for weighted dependence measures

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.6-1
- Initial openEuler RISC-V package from the full package inventory.
