# SPDX-License-Identifier: Apache-2.0
Name:           cinnamon-settings-daemon
Version:        6.6.4
Release:        1%{?dist}
Summary:        Settings daemon for Cinnamon
License:        GPL-2.0-or-later
URL:            https://github.com/linuxmint/cinnamon-settings-daemon
Source0:        cinnamon-settings-daemon-6.6.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Settings daemon for Cinnamon

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING
%license COPYING.LIB
%doc README
%doc README.rst
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.6.4-1
- Initial openEuler RISC-V package from the full package inventory.
