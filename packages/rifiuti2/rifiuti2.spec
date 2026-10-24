# SPDX-License-Identifier: Apache-2.0
Name:           rifiuti2
Version:        0.8.2
Release:        1%{?dist}
Summary:        Tool foranalyzing Windows Recycle Bin INFO2 file.
License:        BSD-3-Clause
URL:            https://github.com/abelcheung/rifiuti2
Source0:        rifiuti2-0.8.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Tool foranalyzing Windows Recycle Bin INFO2 file.

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
%doc NEWS.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.2-1
- Initial openEuler RISC-V package from the full package inventory.
