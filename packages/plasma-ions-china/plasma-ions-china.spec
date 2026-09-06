# SPDX-License-Identifier: Apache-2.0
Name:           plasma-ions-china
Version:        0.1.0
Release:        1%{?dist}
Summary:        A collection of KDE Plasma weather data sources for Chinese users
License:        GPL-3.0-or-later
URL:            https://github.com/arenekosreal/plasma-ions-china
Source0:        plasma-ions-china-0.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A collection of KDE Plasma weather data sources for Chinese users

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
