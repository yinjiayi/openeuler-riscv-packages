# SPDX-License-Identifier: Apache-2.0
Name:           lua53-cffi-lua
Version:        0.2.3
Release:        1%{?dist}
Summary:        A portable C FFI for Lua 5.1+
License:        MIT
URL:            https://github.com/q66/cffi-lua
Source0:        lua53-cffi-lua-0.2.3.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A portable C FFI for Lua 5.1+

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
%license COPYING.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.3-1
- Initial openEuler RISC-V package from the full package inventory.
