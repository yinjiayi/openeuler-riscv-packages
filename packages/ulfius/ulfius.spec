# SPDX-License-Identifier: Apache-2.0
Name:           ulfius
Version:        2.7.15
Release:        1%{?dist}
Summary:        HTTP Framework for REST Applications in C
License:        LGPL-2.1-or-later
URL:            https://github.com/babelouest/ulfius
Source0:        ulfius-2.7.15.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
HTTP Framework for REST Applications in C

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.15-1
- Initial openEuler RISC-V package from the full package inventory.
