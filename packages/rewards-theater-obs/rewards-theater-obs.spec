# SPDX-License-Identifier: Apache-2.0
Name:           rewards-theater-obs
Version:        1.0.8
Release:        1%{?dist}
Summary:        An OBS plugin that lets your viewers redeem videos or sounds on stream via channel points.
License:        GPL-3.0-or-later
URL:            https://github.com/gottagofaster236/RewardsTheater
Source0:        rewards-theater-obs-1.0.8.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
An OBS plugin that lets your viewers redeem videos or sounds on stream via channel points.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.8-1
- Initial openEuler RISC-V package from the full package inventory.
