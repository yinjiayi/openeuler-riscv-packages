# SPDX-License-Identifier: Apache-2.0
Name:           intel-metee
Version:        6.2.5
Release:        1%{?dist}
Summary:        Access library for Intel CSME HECI interface
License:        Apache-2.0
URL:            https://github.com/intel/metee
Source0:        intel-metee-6.2.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Access library for Intel CSME HECI interface

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.2.5-1
- Initial openEuler RISC-V package from the full package inventory.
