# SPDX-License-Identifier: Apache-2.0
Name:           diamond
Version:        2.2.4
Release:        1%{?dist}
Summary:        High performance sequence aligner for protein and translated DNA searches with big sequence data. https://doi.org/10.1038/s41592-021-01101-x
License:        GPL-3.0-or-later
URL:            https://github.com/bbuchfink/diamond
Source0:        diamond-2.2.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
High performance sequence aligner for protein and translated DNA searches with big sequence data. https://doi.org/10.1038/s41592-021-01101-x

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.4-1
- Initial openEuler RISC-V package from the full package inventory.
