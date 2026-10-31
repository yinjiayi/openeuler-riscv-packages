# SPDX-License-Identifier: Apache-2.0
Name:           thc-secure-delete
Version:        3.1.1
Release:        1%{?dist}
Summary:        THC secure deletion tools (srm, sfill, sswap, sdmem)
License:        GPL-2.0-or-later
URL:            https://github.com/gordrs/thc-secure-delete
Source0:        thc-secure-delete-3.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
THC secure deletion tools (srm, sfill, sswap, sdmem)

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
%license COPYRIGHT
%license LICENSE
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
