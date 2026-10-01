# SPDX-License-Identifier: Apache-2.0
Name:           fcitx5-steam-ibus-frontend
Version:        0.0.4
Release:        1%{?dist}
Summary:        Add fcitx5 support for Steam Big Picture session
License:        LGPL-2.1-or-later
URL:            https://github.com/chenx-dust/fcitx5-steam-ibus-frontend
Source0:        fcitx5-steam-ibus-frontend-0.0.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Add fcitx5 support for Steam Big Picture session

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.4-1
- Initial openEuler RISC-V package from the full package inventory.
