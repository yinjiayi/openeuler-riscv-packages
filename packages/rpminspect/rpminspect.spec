# SPDX-License-Identifier: Apache-2.0
Name:           rpminspect
Version:        2.1
Release:        1%{?dist}
Summary:        Build deviation analysis and compliance tool
License:        GPL-3.0-or-later
URL:            https://github.com/rpminspect/rpminspect
Source0:        rpminspect-2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Build deviation analysis and compliance tool

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
%license COPYING
%license COPYING.LIB
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1-1
- Initial openEuler RISC-V package from the full package inventory.
