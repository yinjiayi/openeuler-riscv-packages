# SPDX-License-Identifier: Apache-2.0
Name:           respite
Version:        1.2.1
Release:        1%{?dist}
Summary:        A GTK3 media player (fork of Parole, Xfce deps removed)
License:        GPL-2.0-or-later
URL:            https://github.com/Twilight0/respite
Source0:        respite-1.2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A GTK3 media player (fork of Parole, Xfce deps removed)

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
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
