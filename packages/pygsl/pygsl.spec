# SPDX-License-Identifier: Apache-2.0
Name:           pygsl
Version:        2.6.4
Release:        1%{?dist}
Summary:        GNU Scientific Library Interface for python
License:        GPL-2.0-or-later
URL:            https://github.com/pygsl/pygsl
Source0:        pygsl-2.6.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
GNU Scientific Library Interface for python

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING
%doc README.rst
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.4-1
- Initial openEuler RISC-V package from the full package inventory.
