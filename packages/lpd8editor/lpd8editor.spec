# SPDX-License-Identifier: Apache-2.0
Name:           lpd8editor
Version:        0.0.18
Release:        1%{?dist}
Summary:        A Linux editor for the Akai LPD8 pad controller
License:        MIT
URL:            https://github.com/charlesfleche/lpd8editor
Source0:        lpd8editor-0.0.18.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A Linux editor for the Akai LPD8 pad controller

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
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.18-1
- Initial openEuler RISC-V package from the full package inventory.
