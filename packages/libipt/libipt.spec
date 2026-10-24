# SPDX-License-Identifier: Apache-2.0
Name:           libipt
Version:        2.1.2
Release:        1%{?dist}
Summary:        An Intel(R) Processor Trace decoder library
License:        BSD-3-Clause
URL:            https://github.com/intel/libipt
Source0:        libipt-2.1.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
An Intel(R) Processor Trace decoder library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
