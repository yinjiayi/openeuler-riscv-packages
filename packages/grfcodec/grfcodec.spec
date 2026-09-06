# SPDX-License-Identifier: Apache-2.0
Name:           grfcodec
Version:        6.2.0
Release:        1%{?dist}
Summary:        A tool to convert a GRF file into graphics files and meta data, and vice versa
License:        GPL-2.0-or-later
URL:            https://github.com/OpenTTD/grfcodec
Source0:        grfcodec-6.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A tool to convert a GRF file into graphics files and meta data, and vice versa

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


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
