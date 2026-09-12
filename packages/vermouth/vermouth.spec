# SPDX-License-Identifier: Apache-2.0
Name:           vermouth
Version:        1.9.7
Release:        1%{?dist}
Summary:        A game and app launcher for Linux - native, Windows, and retro
License:        MIT
URL:            https://github.com/dekomote/vermouth
Source0:        vermouth-1.9.7.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A game and app launcher for Linux - native, Windows, and retro

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.7-1
- Initial openEuler RISC-V package from the full package inventory.
