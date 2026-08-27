# SPDX-License-Identifier: Apache-2.0
Name:           nmail
Version:        5.14.12
Release:        1%{?dist}
Summary:        Terminal-based email client
License:        MIT
URL:            https://github.com/d99kris/nmail
Source0:        nmail-5.14.12.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Terminal-based email client

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.14.12-1
- Initial openEuler RISC-V package from the full package inventory.
