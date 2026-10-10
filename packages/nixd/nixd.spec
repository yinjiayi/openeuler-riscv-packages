# SPDX-License-Identifier: Apache-2.0
Name:           nixd
Version:        2.9.2
Release:        1%{?dist}
Summary:        Nix language server
License:        LGPL-3.0-or-later
URL:            https://github.com/nix-community/nixd
Source0:        nixd-2.9.2.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Nix language server

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.9.2-1
- Initial openEuler RISC-V package from the full package inventory.
