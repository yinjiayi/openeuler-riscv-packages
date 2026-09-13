# SPDX-License-Identifier: Apache-2.0
Name:           sqlsmith
Version:        1.5
Release:        1%{?dist}
Summary:        A random SQL query generator
License:        GPL-3.0-or-later
URL:            https://github.com/anse1/sqlsmith
Source0:        sqlsmith-1.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A random SQL query generator

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
%license COPYING


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5-1
- Initial openEuler RISC-V package from the full package inventory.
