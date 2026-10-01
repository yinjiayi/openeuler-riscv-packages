# SPDX-License-Identifier: Apache-2.0
Name:           pstack
Version:        2.17
Release:        1%{?dist}
Summary:        Print stack traces from running processes, or core files.
License:        BSD-2-Clause
URL:            https://github.com/peadar/pstack
Source0:        pstack-2.17.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Print stack traces from running processes, or core files.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.17-1
- Initial openEuler RISC-V package from the full package inventory.
