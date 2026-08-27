# SPDX-License-Identifier: Apache-2.0
Name:           snorenotify
Version:        0.7.0
Release:        1%{?dist}
Summary:        Multi-platform Qt5 notification framework
License:        LGPL-3.0-or-later
URL:            https://github.com/KDE/snorenotify
Source0:        snorenotify-0.7.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Multi-platform Qt5 notification framework

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
%license COPYING.LGPL-3
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
