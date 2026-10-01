# SPDX-License-Identifier: Apache-2.0
Name:           samconf
Version:        0.75.14
Release:        1%{?dist}
Summary:        A c library to manage confiugrations form differnt verified sources
License:        MIT
URL:            https://github.com/Elektrobit/samconf
Source0:        samconf-0.75.14.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A c library to manage confiugrations form differnt verified sources

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.75.14-1
- Initial openEuler RISC-V package from the full package inventory.
