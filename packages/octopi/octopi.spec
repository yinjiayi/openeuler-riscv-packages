# SPDX-License-Identifier: Apache-2.0
Name:           octopi
Version:        0.19.0
Release:        1%{?dist}
Summary:        A powerful Pacman frontend using Qt libs
License:        GPL-2.0-or-later
URL:            https://github.com/aarnt/octopi
Source0:        octopi-0.19.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A powerful Pacman frontend using Qt libs

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
%doc CHANGELOG

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.19.0-1
- Initial openEuler RISC-V package from the full package inventory.
