# SPDX-License-Identifier: Apache-2.0
Name:           custom-toolbox
Version:        26.07
Release:        1%{?dist}
Summary:        A customizable toolbox application built with Qt
License:        GPL-3.0-or-later
URL:            https://github.com/MX-Linux/custom-toolbox
Source0:        custom-toolbox-26.07.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A customizable toolbox application built with Qt

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 26.07-1
- Initial openEuler RISC-V package from the full package inventory.
