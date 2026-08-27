# SPDX-License-Identifier: Apache-2.0
Name:           pcg-cpp
Version:        0.98.1
Release:        1%{?dist}
Summary:        PCG Random Number Generation, C++ Edition
License:        Apache-2.0
URL:            https://github.com/imneme/pcg-cpp
Source0:        pcg-cpp-0.98.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
PCG Random Number Generation, C++ Edition

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.98.1-1
- Initial openEuler RISC-V package from the full package inventory.
