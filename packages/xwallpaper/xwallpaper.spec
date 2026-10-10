# SPDX-License-Identifier: Apache-2.0
Name:           xwallpaper
Version:        0.7.6
Release:        1%{?dist}
Summary:        Wallpaper setting utility for X
License:        ISC
URL:            https://github.com/stoeckmann/xwallpaper
Source0:        xwallpaper-0.7.6.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Wallpaper setting utility for X

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.6-1
- Initial openEuler RISC-V package from the full package inventory.
