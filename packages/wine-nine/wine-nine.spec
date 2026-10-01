# SPDX-License-Identifier: Apache-2.0
Name:           wine-nine
Version:        0.10
Release:        1%{?dist}
Summary:        Gallium Nine Standalone
License:        LGPL-2.1-or-later
URL:            https://github.com/iXit/wine-nine-standalone
Source0:        wine-nine-0.10.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Gallium Nine Standalone

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
%doc README.rst

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10-1
- Initial openEuler RISC-V package from the full package inventory.
