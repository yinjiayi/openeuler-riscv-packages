# SPDX-License-Identifier: Apache-2.0
Name:           mediawriter
Version:        5.3.1
Release:        1%{?dist}
Summary:        Fedora Media Writer - Write Fedora Images to Portable Media
License:        GPL-2.0-or-later
URL:            https://github.com/FedoraQt/MediaWriter
Source0:        mediawriter-5.3.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Fedora Media Writer - Write Fedora Images to Portable Media

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
%license LICENSE.GPL-2
%license LICENSE.LGPL-2
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
