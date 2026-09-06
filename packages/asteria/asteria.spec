# SPDX-License-Identifier: Apache-2.0
Name:           asteria
Version:        2.4.7
Release:        1%{?dist}
Summary:        Astrological chart calculator and analyzer with AI interpretations
License:        AGPL-3.0
URL:            https://github.com/alamahant/Asteria
Source0:        asteria-2.4.7.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Astrological chart calculator and analyzer with AI interpretations

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.7-1
- Initial openEuler RISC-V package from the full package inventory.
