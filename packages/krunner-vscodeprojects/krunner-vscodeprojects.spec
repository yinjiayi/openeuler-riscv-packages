# SPDX-License-Identifier: Apache-2.0
Name:           krunner-vscodeprojects
Version:        2.0.2
Release:        1%{?dist}
Summary:        Open VSCode Project Manager projects from Krunner
License:        LGPL-3.0-or-later
URL:            https://github.com/alex1701c/krunner-vscodeprojects
Source0:        krunner-vscodeprojects-2.0.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Open VSCode Project Manager projects from Krunner

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
