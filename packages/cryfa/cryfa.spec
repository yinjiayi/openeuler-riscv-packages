# SPDX-License-Identifier: Apache-2.0
Name:           cryfa
Version:        20.04
Release:        1%{?dist}
Summary:        A secure encryption tool for genomic data
License:        GPL-3.0-or-later
URL:            https://github.com/cobilab/cryfa
Source0:        cryfa-20.04.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A secure encryption tool for genomic data

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 20.04-1
- Initial openEuler RISC-V package from the full package inventory.
