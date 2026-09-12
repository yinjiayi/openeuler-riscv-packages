# SPDX-License-Identifier: Apache-2.0
Name:           lightbase
Version:        1.0.0
Release:        1%{?dist}
Summary:        A sovereign, high-performance API development ecosystem.
License:        Apache-2.0
URL:            https://github.com/Aarav90-cpu/LightBase
Source0:        lightbase-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A sovereign, high-performance API development ecosystem.

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
