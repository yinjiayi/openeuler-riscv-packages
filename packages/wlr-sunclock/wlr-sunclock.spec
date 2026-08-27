# SPDX-License-Identifier: Apache-2.0
Name:           wlr-sunclock
Version:        1.2.1
Release:        1%{?dist}
Summary:        Displays a sunclock desktop widget using the layer shell protocol
License:        LGPL-3.0-or-later
URL:            https://github.com/sentriz/wlr-sunclock
Source0:        wlr-sunclock-1.2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Displays a sunclock desktop widget using the layer shell protocol

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
%license LICENCE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
