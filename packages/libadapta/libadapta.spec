# SPDX-License-Identifier: Apache-2.0
Name:           libadapta
Version:        1.5.0
Release:        1%{?dist}
Summary:        libAdapta is libAdwaita with theme support and a few extra.
License:        LGPL-2.1-or-later
URL:            https://github.com/xapp-project/libadapta
Source0:        libadapta-1.5.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
libAdapta is libAdwaita with theme support and a few extra.

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
%doc NEWS
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
