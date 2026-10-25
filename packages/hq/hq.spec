# SPDX-License-Identifier: Apache-2.0
Name:           hq
Version:        3.2
Release:        1%{?dist}
Summary:        HTML processor inspired by jq
License:        AGPL-3.0
URL:            https://github.com/coderobe/hq
Source0:        hq-3.2.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
HTML processor inspired by jq

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
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-1
- Initial openEuler RISC-V package from the full package inventory.
