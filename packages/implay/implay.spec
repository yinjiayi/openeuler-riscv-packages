# SPDX-License-Identifier: Apache-2.0
Name:           implay
Version:        1.5.1
Release:        1%{?dist}
Summary:        Desktop media player built on top of mpv and imgui
License:        GPL-2.0-or-later
URL:            https://github.com/tsl0922/ImPlay
Source0:        implay-1.5.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Desktop media player built on top of mpv and imgui

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
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-1
- Initial openEuler RISC-V package from the full package inventory.
