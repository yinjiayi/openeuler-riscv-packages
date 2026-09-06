# SPDX-License-Identifier: Apache-2.0
Name:           spi-tools
Version:        1.1.0
Release:        1%{?dist}
Summary:        A set of SPI tools for Linux
License:        GPL-2.0-or-later
URL:            https://github.com/cpb-/spi-tools
Source0:        spi-tools-1.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A set of SPI tools for Linux

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
