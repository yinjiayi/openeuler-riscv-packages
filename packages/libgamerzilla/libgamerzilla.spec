# SPDX-License-Identifier: Apache-2.0
Name:           libgamerzilla
Version:        0.1.3
Release:        1%{?dist}
Summary:        Gamerzilla Integration Library
License:        Zlib
URL:            https://github.com/dulsi/libgamerzilla
Source0:        libgamerzilla-0.1.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Gamerzilla Integration Library

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
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.3-1
- Initial openEuler RISC-V package from the full package inventory.
