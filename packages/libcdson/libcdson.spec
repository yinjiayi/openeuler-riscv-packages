# SPDX-License-Identifier: Apache-2.0
Name:           libcdson
Version:        1.0.0
Release:        1%{?dist}
Summary:        Pure C parsing/serialization for the DSON data format, for humans
License:        MPL-2.0
URL:            https://github.com/frozencemetery/cdson
Source0:        libcdson-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Pure C parsing/serialization for the DSON data format, for humans

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
