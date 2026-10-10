# SPDX-License-Identifier: Apache-2.0
Name:           liblastfm-qt5
Version:        1.1.0
Release:        1%{?dist}
Summary:        A Qt C++ Library for the Last.fm Webservices
License:        GPL-3.0-or-later
URL:            https://github.com/lastfm/liblastfm
Source0:        liblastfm-qt5-1.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A Qt C++ Library for the Last.fm Webservices

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
