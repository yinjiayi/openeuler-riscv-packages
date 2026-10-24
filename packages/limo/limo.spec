# SPDX-License-Identifier: Apache-2.0
Name:           limo
Version:        1.2.2
Release:        1%{?dist}
Summary:        A simple Qt based mod manager
License:        GPL-3.0-or-later
URL:            https://github.com/limo-app/limo
Source0:        limo-1.2.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A simple Qt based mod manager

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
