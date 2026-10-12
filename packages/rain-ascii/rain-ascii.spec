# SPDX-License-Identifier: Apache-2.0
Name:           rain-ascii
Version:        0.2.0
Release:        1%{?dist}
Summary:        Comfy ASCII rain for your terminal
License:        MIT
URL:            https://github.com/cursssed/rain
Source0:        rain-ascii-0.2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Comfy ASCII rain for your terminal

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
