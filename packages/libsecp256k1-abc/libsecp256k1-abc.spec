# SPDX-License-Identifier: Apache-2.0
Name:           libsecp256k1-abc
Version:        0.27.1
Release:        1%{?dist}
Summary:        Optimized C library for EC operations on curve secp256k1
License:        MIT
URL:            https://github.com/Bitcoin-ABC/secp256k1
Source0:        libsecp256k1-abc-0.27.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Optimized C library for EC operations on curve secp256k1

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.27.1-1
- Initial openEuler RISC-V package from the full package inventory.
