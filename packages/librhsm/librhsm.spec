# SPDX-License-Identifier: Apache-2.0
Name:           librhsm
Version:        0.0.4
Release:        1%{?dist}
Summary:        Red Hat Subscription Manager library
License:        LGPL-2.1-or-later
URL:            https://github.com/rpm-software-management/librhsm
Source0:        librhsm-0.0.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Red Hat Subscription Manager library

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.4-1
- Initial openEuler RISC-V package from the full package inventory.
