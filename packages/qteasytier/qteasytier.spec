# SPDX-License-Identifier: Apache-2.0
Name:           qteasytier
Version:        3.0.2
Release:        1%{?dist}
Summary:        基于 EasyTier, 一款美观实用的远程联机工具!
License:        LGPL-3.0-or-later
URL:            https://github.com/qteasytier/qt-easy-tier
Source0:        qteasytier-3.0.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
基于 EasyTier, 一款美观实用的远程联机工具!

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
