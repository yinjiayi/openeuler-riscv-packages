# SPDX-License-Identifier: Apache-2.0
Name:           ditrigon
Version:        1.6.0
Release:        1%{?dist}
Summary:        A popular and easy to use graphical IRC (chat) client
License:        GPL-2.0-or-later
URL:            https://github.com/bluewww/ditrigon
Source0:        ditrigon-1.6.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A popular and easy to use graphical IRC (chat) client

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


%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
