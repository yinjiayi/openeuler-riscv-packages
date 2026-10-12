# SPDX-License-Identifier: Apache-2.0
Name:           brlaser
Version:        6.2.8
Release:        1%{?dist}
Summary:        Brother laser printer driver
License:        GPL-2.0-or-later
URL:            https://github.com/Owl-Maintain/brlaser
Source0:        brlaser-6.2.8.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Brother laser printer driver

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
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.2.8-1
- Initial openEuler RISC-V package from the full package inventory.
