# SPDX-License-Identifier: Apache-2.0
Name:           libvarlink
Version:        24.0.1
Release:        1%{?dist}
Summary:        Varlink C library and command line tool
License:        Apache-2.0
URL:            https://github.com/varlink/libvarlink
Source0:        libvarlink-24.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Varlink C library and command line tool

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 24.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
