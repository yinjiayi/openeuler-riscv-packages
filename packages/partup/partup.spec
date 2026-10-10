# SPDX-License-Identifier: Apache-2.0
Name:           partup
Version:        3.0.1
Release:        1%{?dist}
Summary:        System initialization program formatting and writing flash devices
License:        GPL-3.0-or-later
URL:            https://github.com/phytec/partup
Source0:        partup-3.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
System initialization program formatting and writing flash devices

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
