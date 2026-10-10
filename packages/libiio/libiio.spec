# SPDX-License-Identifier: Apache-2.0
Name:           libiio
Version:        0.26
Release:        1%{?dist}
Summary:        Interface to the Linux Industrial Input/Output (IIO) Subsystem
License:        LGPL-2.1-or-later
URL:            https://github.com/analogdevicesinc/libiio
Source0:        libiio-0.26.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Interface to the Linux Industrial Input/Output (IIO) Subsystem

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
%license COPYING.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.26-1
- Initial openEuler RISC-V package from the full package inventory.
