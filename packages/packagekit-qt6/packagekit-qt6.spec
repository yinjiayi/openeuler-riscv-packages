# SPDX-License-Identifier: Apache-2.0
Name:           packagekit-qt6
Version:        1.1.4
Release:        1%{?dist}
Summary:        Simple software installation management software
License:        LGPL-2.1-or-later
URL:            https://github.com/hughsie/PackageKit-Qt
Source0:        packagekit-qt6-1.1.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Simple software installation management software

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
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.4-1
- Initial openEuler RISC-V package from the full package inventory.
