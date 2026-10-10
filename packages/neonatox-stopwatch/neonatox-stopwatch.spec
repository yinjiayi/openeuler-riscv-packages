# SPDX-License-Identifier: Apache-2.0
Name:           neonatox-stopwatch
Version:        1.0.0
Release:        1%{?dist}
Summary:        A simple gtk 4 stopwatch.
License:        GPL-3.0-or-later
URL:            https://github.com/cargabsj175/neonatox-stopwatch
Source0:        neonatox-stopwatch-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A simple gtk 4 stopwatch.

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
