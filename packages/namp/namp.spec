# SPDX-License-Identifier: Apache-2.0
Name:           namp
Version:        2.57
Release:        1%{?dist}
Summary:        Terminal-based audio player
License:        GPL-2.0-or-later
URL:            https://github.com/d99kris/namp
Source0:        namp-2.57.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Terminal-based audio player

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.57-1
- Initial openEuler RISC-V package from the full package inventory.
