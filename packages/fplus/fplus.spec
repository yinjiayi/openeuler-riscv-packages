# SPDX-License-Identifier: Apache-2.0
Name:           fplus
Version:        0.2.25
Release:        1%{?dist}
Summary:        Functional Programming Library for C++
License:        BSL-1.0
URL:            https://github.com/Dobiasd/FunctionalPlus
Source0:        fplus-0.2.25.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Functional Programming Library for C++

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.25-1
- Initial openEuler RISC-V package from the full package inventory.
