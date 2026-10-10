# SPDX-License-Identifier: Apache-2.0
Name:           lua-lua-template
Version:        1.0.0
Release:        1%{?dist}
Summary:        Efficient template engine for Lua
License:        MIT
URL:            https://github.com/anaef/lua-template
Source0:        lua-lua-template-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Efficient template engine for Lua

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc NEWS.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
