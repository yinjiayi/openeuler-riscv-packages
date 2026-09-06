# SPDX-License-Identifier: Apache-2.0
Name:           openrc
Version:        0.63
Release:        1%{?dist}
Summary:        Dependency based init system that works with sysvinit and systemd or on its own.
License:        BSD-2-Clause
URL:            https://github.com/OpenRC/openrc
Source0:        openrc-0.63.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Dependency based init system that works with sysvinit and systemd or on its own.

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
%doc NEWS.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.63-1
- Initial openEuler RISC-V package from the full package inventory.
