# SPDX-License-Identifier: Apache-2.0
Name:           lapifetch
Version:        1.4.0
Release:        1%{?dist}
Summary:        Simple bunny-themed Linux fetch utility
License:        MIT
URL:            https://github.com/asunyan-dev/lapifetch
Source0:        lapifetch-1.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Simple bunny-themed Linux fetch utility

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


%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
