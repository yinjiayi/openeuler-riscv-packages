# SPDX-License-Identifier: Apache-2.0
Name:           jasmine
Version:        1.3.3
Release:        1%{?dist}
Summary:        Website launcher and session management platform with profiles for each tab plus Internet radio, IPTV and podcasts support.
License:        GPL-3.0-or-later
URL:            https://github.com/alamahant/Jasmine
Source0:        jasmine-1.3.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Website launcher and session management platform with profiles for each tab plus Internet radio, IPTV and podcasts support.

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.3-1
- Initial openEuler RISC-V package from the full package inventory.
