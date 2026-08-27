# SPDX-License-Identifier: Apache-2.0
Name:           rofi-emoji
Version:        4.1.0
Release:        1%{?dist}
Summary:        A Rofi plugin for selecting emojis
License:        MIT
URL:            https://github.com/Mange/rofi-emoji
Source0:        rofi-emoji-4.1.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A Rofi plugin for selecting emojis

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
