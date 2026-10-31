# SPDX-License-Identifier: Apache-2.0
Name:           mdns
Version:        1.4.3
Release:        1%{?dist}
Summary:        Cross-platform mDNS/DNS-SD library in C
License:        Unlicense
URL:            https://github.com/mjansson/mdns
Source0:        mdns-1.4.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Cross-platform mDNS/DNS-SD library in C

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
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.3-1
- Initial openEuler RISC-V package from the full package inventory.
