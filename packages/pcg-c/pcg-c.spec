# SPDX-License-Identifier: Apache-2.0
Name:           pcg-c
Version:        0.94.2
Release:        1%{?dist}
Summary:        PCG random number generation library for C
License:        Apache-2.0
URL:            https://github.com/andy5995/pcg-c
Source0:        pcg-c-0.94.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
PCG random number generation library for C

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license LICENSE.spdx
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.94.2-1
- Initial openEuler RISC-V package from the full package inventory.
