# SPDX-License-Identifier: Apache-2.0
Name:           libzstd-seek
Version:        1.3.0
Release:        1%{?dist}
Summary:        A library that mimic fread, fseek and ftell for reading zstd compressed files.
License:        MIT
URL:            https://github.com/martinellimarco/libzstd-seek
Source0:        libzstd-seek-1.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A library that mimic fread, fseek and ftell for reading zstd compressed files.

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
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
