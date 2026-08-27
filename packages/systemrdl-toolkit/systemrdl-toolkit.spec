# SPDX-License-Identifier: Apache-2.0
Name:           systemrdl-toolkit
Version:        0.3.0
Release:        1%{?dist}
Summary:        A pure C++ toolkit for parsing and elaborating SystemRDL files
License:        MIT
URL:            https://github.com/vowstar/systemrdl-toolkit
Source0:        systemrdl-toolkit-0.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A pure C++ toolkit for parsing and elaborating SystemRDL files

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
