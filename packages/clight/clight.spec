# SPDX-License-Identifier: Apache-2.0
Name:           clight
Version:        4.11
Release:        1%{?dist}
Summary:        A C daemon that turns your webcam into a light sensor. It can also change display gamma temperature, dim your screen and set your dpms.
License:        GPL-3.0-or-later
URL:            https://github.com/FedeDP/Clight
Source0:        clight-4.11.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A C daemon that turns your webcam into a light sensor. It can also change display gamma temperature, dim your screen and set your dpms.

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.11-1
- Initial openEuler RISC-V package from the full package inventory.
