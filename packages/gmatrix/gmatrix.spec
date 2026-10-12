# SPDX-License-Identifier: Apache-2.0
Name:           gmatrix
Version:        2.0.1
Release:        1%{?dist}
Summary:        A fast and lightweight terminal entertainment program for Matrix rain
License:        GPL-3.0-or-later
URL:            https://github.com/gducpm/gmatrix
Source0:        gmatrix-2.0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A fast and lightweight terminal entertainment program for Matrix rain

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
