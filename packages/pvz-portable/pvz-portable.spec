# SPDX-License-Identifier: Apache-2.0
Name:           pvz-portable
Version:        0.2.0
Release:        1%{?dist}
Summary:        A cross-platform community-driven reimplementation of Plants vs. Zombies: Game of the Year Edition, aiming to bring the 100%% authentic PvZ experience to eve
License:        LGPL-3.0-or-later
URL:            https://github.com/wszqkzqk/pvz-portable
Source0:        pvz-portable-0.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A cross-platform community-driven reimplementation of Plants vs. Zombies: Game of the Year Edition, aiming to bring the 100%% authentic PvZ experience to eve

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
%license COPYING
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
