# SPDX-License-Identifier: Apache-2.0
Name:           xkb-switch
Version:        1.8.5
Release:        1%{?dist}
Summary:        Program that allows to query and change the XKB layout state
License:        MIT
URL:            https://github.com/grwlf/xkb-switch
Source0:        xkb-switch-1.8.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Program that allows to query and change the XKB layout state

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
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.5-1
- Initial openEuler RISC-V package from the full package inventory.
