# SPDX-License-Identifier: Apache-2.0
Name:           loderunner-ng
Version:        0.1.4
Release:        1%{?dist}
Summary:        Classic Lode Runner game remake
License:        GPL-3.0-or-later
URL:            https://github.com/vchimishuk/loderunner-ng
Source0:        loderunner-ng-0.1.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Classic Lode Runner game remake

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
%doc README
%doc README.md
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.4-1
- Initial openEuler RISC-V package from the full package inventory.
