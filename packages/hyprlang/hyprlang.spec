# SPDX-License-Identifier: Apache-2.0
Name:           hyprlang
Version:        0.6.8
Release:        1%{?dist}
Summary:        implementation library for the hypr config language
License:        LGPL-3.0-or-later
URL:            https://github.com/hyprwm/hyprlang
Source0:        hyprlang-0.6.8.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
implementation library for the hypr config language

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
%license COPYRIGHT
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.8-1
- Initial openEuler RISC-V package from the full package inventory.
