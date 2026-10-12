# SPDX-License-Identifier: Apache-2.0
Name:           codec2
Version:        1.2.0
Release:        1%{?dist}
Summary:        Open source speech codec designed for communications quality speech between 450 and 3200 bit/s
License:        LGPL-2.1-or-later
URL:            https://github.com/drowe67/codec2
Source0:        codec2-1.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Open source speech codec designed for communications quality speech between 450 and 3200 bit/s

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
