# SPDX-License-Identifier: Apache-2.0
Name:           linyaps-web-store-installer
Version:        1.6.8
Release:        1%{?dist}
Summary:        玲珑（Linglong）linyaps-web-store-installer is a package installer for the Linyaps Web store.
License:        LGPL-3.0-or-later
URL:            https://github.com/OpenAtom-Linyaps/linyaps-web-store-installer
Source0:        linyaps-web-store-installer-1.6.8.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
玲珑（Linglong）linyaps-web-store-installer is a package installer for the Linyaps Web store.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.8-1
- Initial openEuler RISC-V package from the full package inventory.
