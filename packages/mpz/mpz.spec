# SPDX-License-Identifier: Apache-2.0
Name:           mpz
Version:        2.1.2
Release:        2%{?dist}
Summary:        Music player for the large local collections
License:        GPL-3.0-or-later
URL:            https://github.com/olegantonyan/mpz
Source0:        mpz-2.1.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  gtest-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  taglib-devel
BuildRequires:  yaml-cpp-devel

%description
Music player for the large local collections

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license license.txt
%doc README.md

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-2
- Raise the bounded QEMU build timeout to 180 minutes after exact-head CI
  compiled normally to 50% before the 60-minute package budget expired.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the Qt 6, test, and media metadata development files required by CMake.
