# SPDX-License-Identifier: Apache-2.0
Name:           bamtools
Version:        2.5.3
Release:        1%{?dist}
Summary:        C++ API & command-line toolkit for working with BAM data
License:        MIT
URL:            https://github.com/pezmaster31/bamtools
Source0:        bamtools-2.5.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ API & command-line toolkit for working with BAM data

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.3-1
- Initial openEuler RISC-V package from the full package inventory.
