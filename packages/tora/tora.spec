# SPDX-License-Identifier: Apache-2.0
Name:           tora
Version:        3.2
Release:        1%{?dist}
Summary:        SQL IDE for Oracle, MySQL and PostgreSQL dbs
License:        GPL-2.0-or-later
URL:            https://github.com/tora-tool/tora
Source0:        tora-3.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
SQL IDE for Oracle, MySQL and PostgreSQL dbs

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
%license COPYING
%license COPYING.RTF
%license copyright.txt
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-1
- Initial openEuler RISC-V package from the full package inventory.
