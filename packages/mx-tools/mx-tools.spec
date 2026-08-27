# SPDX-License-Identifier: Apache-2.0
Name:           mx-tools
Version:        26.06
Release:        1%{?dist}
Summary:        MX Tools - Dashboard application launcher for various MX tools
License:        GPL-3.0-or-later
URL:            https://github.com/MX-Linux/mx-tools
Source0:        mx-tools-26.06.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
MX Tools - Dashboard application launcher for various MX tools

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 26.06-1
- Initial openEuler RISC-V package from the full package inventory.
