# SPDX-License-Identifier: Apache-2.0
Name:           criterion
Version:        2.4.3
Release:        1%{?dist}
Summary:        A cross-platform C and C++ unit testing framework for the 21st century
License:        MIT
URL:            https://github.com/Snaipe/Criterion
Source0:        criterion-2.4.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A cross-platform C and C++ unit testing framework for the 21st century

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
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.3-1
- Initial openEuler RISC-V package from the full package inventory.
