# SPDX-License-Identifier: Apache-2.0
Name:           gr-rds
Version:        3.10
Release:        1%{?dist}
Summary:        GNU Radio FM RDS Receiver
License:        GPL-3.0-or-later
URL:            https://github.com/bastibl/gr-rds
Source0:        gr-rds-3.10.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
GNU Radio FM RDS Receiver

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.10-1
- Initial openEuler RISC-V package from the full package inventory.
