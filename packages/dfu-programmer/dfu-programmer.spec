# SPDX-License-Identifier: Apache-2.0
Name:           dfu-programmer
Version:        1.1.0
Release:        1%{?dist}
Summary:        dfu-programmer is a Device Firmware Update based USB programmer for Atmel chips with a USB bootloader
License:        GPL-2.0-or-later
URL:            https://github.com/dfu-programmer/dfu-programmer
Source0:        dfu-programmer-1.1.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
dfu-programmer is a Device Firmware Update based USB programmer for Atmel chips with a USB bootloader

%prep
%autosetup -p1

%build
autoreconf -fi
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
%doc README.md
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
