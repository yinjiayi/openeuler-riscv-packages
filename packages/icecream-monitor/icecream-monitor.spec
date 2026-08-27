# SPDX-License-Identifier: Apache-2.0
Name:           icecream-monitor
Version:        3.3
Release:        1%{?dist}
Summary:        Monitor Program for the icecream Compile Farm
License:        GPL-2.0-or-later
URL:            https://github.com/icecc/icemon
Source0:        icecream-monitor-3.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Monitor Program for the icecream Compile Farm

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3-1
- Initial openEuler RISC-V package from the full package inventory.
