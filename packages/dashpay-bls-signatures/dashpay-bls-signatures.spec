# SPDX-License-Identifier: Apache-2.0
Name:           dashpay-bls-signatures
Version:        1.3.5
Release:        1%{?dist}
Summary:        Chia Networks BLS Signatures implementation fork for Dashcore
License:        Apache-2.0
URL:            https://github.com/dashpay/bls-signatures
Source0:        dashpay-bls-signatures-1.3.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Chia Networks BLS Signatures implementation fork for Dashcore

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.5-1
- Initial openEuler RISC-V package from the full package inventory.
