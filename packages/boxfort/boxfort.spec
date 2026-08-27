# SPDX-License-Identifier: Apache-2.0
Name:           boxfort
Version:        0.1.5
Release:        1%{?dist}
Summary:        A sandboxing C library for Criterion
License:        MIT
URL:            https://github.com/Snaipe/BoxFort
Source0:        boxfort-0.1.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A sandboxing C library for Criterion

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.5-1
- Initial openEuler RISC-V package from the full package inventory.
