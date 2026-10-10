# SPDX-License-Identifier: Apache-2.0
Name:           wl-gammarelay
Version:        0.1.3
Release:        1%{?dist}
Summary:        A client and daemon for changing color temperature and brightness under Wayland via keybindings.
License:        GPL-3.0-or-later
URL:            https://github.com/jeremija/wl-gammarelay
Source0:        wl-gammarelay-0.1.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A client and daemon for changing color temperature and brightness under Wayland via keybindings.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.3-1
- Initial openEuler RISC-V package from the full package inventory.
