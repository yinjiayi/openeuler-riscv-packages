# SPDX-License-Identifier: Apache-2.0
Name:           hoel
Version:        1.4.29
Release:        1%{?dist}
Summary:        C Database abstraction library with json based language
License:        LGPL-2.1-or-later
URL:            https://github.com/babelouest/hoel
Source0:        hoel-1.4.29.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
C Database abstraction library with json based language

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.29-1
- Initial openEuler RISC-V package from the full package inventory.
