# SPDX-License-Identifier: Apache-2.0
Name:           bongocat
Version:        2.0.2
Release:        1%{?dist}
Summary:        Delightful Wayland overlay that displays an animated bongo cat reacting to keyboard input
License:        MIT
URL:            https://github.com/saatvik333/wayland-bongocat
Source0:        bongocat-2.0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Delightful Wayland overlay that displays an animated bongo cat reacting to keyboard input

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
