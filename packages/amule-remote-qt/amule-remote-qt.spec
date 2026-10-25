# SPDX-License-Identifier: Apache-2.0
Name:           amule-remote-qt
Version:        0.1.3
Release:        1%{?dist}
Summary:        Qt remote control for the aMule daemon over the EC protocol
License:        GPL-3.0-or-later
URL:            https://github.com/manuel-alcocer/amule-remote-qt
Source0:        amule-remote-qt-0.1.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Qt remote control for the aMule daemon over the EC protocol

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.3-1
- Initial openEuler RISC-V package from the full package inventory.
