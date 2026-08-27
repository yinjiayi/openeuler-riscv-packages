# SPDX-License-Identifier: Apache-2.0
Name:           qman
Version:        1.5.1
Release:        1%{?dist}
Summary:        A more modern manual page viewer for our terminals
License:        BSD-2-Clause
URL:            https://github.com/plp13/qman
Source0:        qman-1.5.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A more modern manual page viewer for our terminals

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-1
- Initial openEuler RISC-V package from the full package inventory.
