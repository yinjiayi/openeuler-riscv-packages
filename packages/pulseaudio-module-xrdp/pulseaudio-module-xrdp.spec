# SPDX-License-Identifier: Apache-2.0
Name:           pulseaudio-module-xrdp
Version:        0.8
Release:        1%{?dist}
Summary:        xrdp pulseaudio module
License:        LGPL-2.1-or-later
URL:            https://github.com/neutrinolabs/pulseaudio-module-xrdp
Source0:        pulseaudio-module-xrdp-0.8.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
xrdp pulseaudio module

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8-1
- Initial openEuler RISC-V package from the full package inventory.
