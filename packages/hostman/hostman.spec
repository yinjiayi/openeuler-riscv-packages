# SPDX-License-Identifier: Apache-2.0
Name:           hostman
Version:        1.2.5
Release:        1%{?dist}
Summary:        A simple file host manager for various image hosting services
License:        MIT
URL:            https://github.com/keircn/hostman
Source0:        hostman-1.2.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A simple file host manager for various image hosting services

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.5-1
- Initial openEuler RISC-V package from the full package inventory.
