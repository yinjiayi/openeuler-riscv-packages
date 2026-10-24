# SPDX-License-Identifier: Apache-2.0
Name:           mx-locale
Version:        26.03
Release:        1%{?dist}
Summary:        GUI configuration tool for locales
License:        LGPL-3.0-or-later
URL:            https://github.com/MX-Linux/mx-locale
Source0:        mx-locale-26.03.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
GUI configuration tool for locales

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
%license license.html
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 26.03-1
- Initial openEuler RISC-V package from the full package inventory.
