# SPDX-License-Identifier: Apache-2.0
Name:           bluealsa
Version:        4.3.1
Release:        1%{?dist}
Summary:        Bluetooth audio ALSA backend
License:        MIT
URL:            https://github.com/Arkq/bluez-alsa
Source0:        bluealsa-4.3.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Bluetooth audio ALSA backend

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
%license LICENSE
%doc README.md
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
