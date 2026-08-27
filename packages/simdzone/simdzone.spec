# SPDX-License-Identifier: Apache-2.0
Name:           simdzone
Version:        0.2.4
Release:        1%{?dist}
Summary:        Fast and standards compliant DNS presentation format parser
License:        BSD-3-Clause
URL:            https://github.com/NLnetLabs/simdzone
Source0:        simdzone-0.2.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Fast and standards compliant DNS presentation format parser

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.4-1
- Initial openEuler RISC-V package from the full package inventory.
