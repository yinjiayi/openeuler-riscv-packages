# SPDX-License-Identifier: Apache-2.0
Name:           pinentry-hypr
Version:        0.1.0
Release:        1%{?dist}
Summary:        A Hyprland-native GnuPG pinentry using Qt6/QML/hyprutils
License:        BSD-3-Clause
URL:            https://github.com/AuthenticSm1les/pinentry-hypr
Source0:        pinentry-hypr-0.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A Hyprland-native GnuPG pinentry using Qt6/QML/hyprutils

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
