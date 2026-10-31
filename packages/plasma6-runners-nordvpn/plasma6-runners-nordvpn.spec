# SPDX-License-Identifier: Apache-2.0
Name:           plasma6-runners-nordvpn
Version:        3.2.1
Release:        1%{?dist}
Summary:        Nordvpn plasma 6 runner
License:        LGPL-3.0-or-later
URL:            https://github.com/alex1701c/NordVPNKrunner
Source0:        plasma6-runners-nordvpn-3.2.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Nordvpn plasma 6 runner

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
