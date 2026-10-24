# SPDX-License-Identifier: Apache-2.0
Name:           ksnip
Version:        1.10.1
Release:        1%{?dist}
Summary:        Qt-based screenshot tool that provides many annotation features
License:        GPL-3.0-or-later
URL:            https://github.com/ksnip/ksnip
Source0:        ksnip-1.10.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Qt-based screenshot tool that provides many annotation features

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
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10.1-1
- Initial openEuler RISC-V package from the full package inventory.
