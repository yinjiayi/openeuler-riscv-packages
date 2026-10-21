# SPDX-License-Identifier: Apache-2.0
Name:           usbtop
Version:        1.0
Release:        1%{?dist}
Summary:        top-like utility that shows an estimated instantaneous bandwidth on USB buses and devices
License:        BSD-3-Clause
URL:            https://github.com/aguinet/usbtop
Source0:        usbtop-1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
top-like utility that shows an estimated instantaneous bandwidth on USB buses and devices

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0-1
- Initial openEuler RISC-V package from the full package inventory.
