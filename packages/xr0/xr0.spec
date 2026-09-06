# SPDX-License-Identifier: Apache-2.0
Name:           xr0
Version:        0.18.0
Release:        1%{?dist}
Summary:        A verifier for C that aims to guarantee the safety of C programs at compile time
License:        Apache-2.0
URL:            https://github.com/xr0-org/xr0
Source0:        xr0-0.18.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A verifier for C that aims to guarantee the safety of C programs at compile time

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.18.0-1
- Initial openEuler RISC-V package from the full package inventory.
