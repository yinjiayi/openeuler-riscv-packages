# SPDX-License-Identifier: Apache-2.0
Name:           milton
Version:        1.9.1
Release:        1%{?dist}
Summary:        An infinite-canvas paint program
License:        GPL-3.0-or-later
URL:            https://github.com/serge-rgb/milton
Source0:        milton-1.9.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtk2-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  make
BuildRequires:  mesa-libGL-devel

%description
An infinite-canvas paint program

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.1-1
- Initial openEuler RISC-V package from the full package inventory.
