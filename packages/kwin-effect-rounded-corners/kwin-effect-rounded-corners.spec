# SPDX-License-Identifier: Apache-2.0
Name:           kwin-effect-rounded-corners
Version:        0.9.0
Release:        1%{?dist}
Summary:        Rounds the corners of your windows (wayland)
License:        GPL-3.0-or-later
URL:            https://github.com/matinlotfali/KDE-Rounded-Corners
Source0:        kwin-effect-rounded-corners-0.9.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Rounds the corners of your windows (wayland)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.0-1
- Initial openEuler RISC-V package from the full package inventory.
