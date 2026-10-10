# SPDX-License-Identifier: Apache-2.0
Name:           fcitx5-pinboard
Version:        0.1.0
Release:        1%{?dist}
Summary:        Fcitx5 clipboard history addon with pinning, using the native candidate window
License:        LGPL-2.1-or-later
URL:            https://github.com/7-1/fcitx5-pinboard
Source0:        fcitx5-pinboard-0.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Fcitx5 clipboard history addon with pinning, using the native candidate window

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
