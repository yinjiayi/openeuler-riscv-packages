# SPDX-License-Identifier: Apache-2.0
Name:           mcalc
Version:        3.0.0
Release:        1%{?dist}
Summary:        MCalc - calculator for performing simple mathematical operations in all existing number systems
License:        MIT
URL:            https://github.com/nesterovmaxim31/MCalc
Source0:        mcalc-3.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
MCalc - calculator for performing simple mathematical operations in all existing number systems

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
