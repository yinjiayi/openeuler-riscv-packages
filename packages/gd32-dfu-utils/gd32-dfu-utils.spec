# SPDX-License-Identifier: Apache-2.0
Name:           gd32-dfu-utils
Version:        0.9
Release:        1%{?dist}
Summary:        Dfu-utils GD32 fork. Dfu-util - Device Firmware Upgrade Utilities
License:        GPL-2.0-or-later
URL:            https://github.com/riscv-mcu/gd32-dfu-utils
Source0:        gd32-dfu-utils-0.9.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Dfu-utils GD32 fork. Dfu-util - Device Firmware Upgrade Utilities

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
%license COPYING
%doc README
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9-1
- Initial openEuler RISC-V package from the full package inventory.
