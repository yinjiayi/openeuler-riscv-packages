# SPDX-License-Identifier: Apache-2.0
Name:           heimer
Version:        4.5.0
Release:        2%{?dist}
Summary:        Cross-platform mind map, diagram, and note-taking tool
License:        GPL-3.0-or-later
URL:            https://github.com/juzzlin/heimer
Source0:        heimer-4.5.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel

%description
Cross-platform mind map, diagram, and note-taking tool

%prep
%autosetup -n Heimer-%{version} -p1

%build
%cmake -DBUILD_TESTS=ON
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
%doc AUTHORS
%doc CHANGELOG

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.5.0-2
- Match the case-preserving GitHub archive root and declare the complete Qt5 build closure.
- Enable Heimer's actual BUILD_TESTS option so the full upstream suite remains active.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
