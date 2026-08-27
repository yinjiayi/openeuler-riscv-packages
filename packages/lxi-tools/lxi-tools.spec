# SPDX-License-Identifier: Apache-2.0
Name:           lxi-tools
Version:        2.8
Release:        1%{?dist}
Summary:        LXI Tools is a collection of software tools for controlling LXI instruments
License:        BSD-3-Clause
URL:            https://github.com/lxi/lxi-tools
Source0:        lxi-tools-2.8.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
LXI Tools is a collection of software tools for controlling LXI instruments

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
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8-1
- Initial openEuler RISC-V package from the full package inventory.
