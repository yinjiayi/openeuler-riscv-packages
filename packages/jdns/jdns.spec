# SPDX-License-Identifier: Apache-2.0
Name:           jdns
Version:        2.0.6
Release:        1%{?dist}
Summary:        A simple DNS queries library
License:        MIT
URL:            https://github.com/psi-im/jdns
Source0:        jdns-2.0.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A simple DNS queries library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.6-1
- Initial openEuler RISC-V package from the full package inventory.
