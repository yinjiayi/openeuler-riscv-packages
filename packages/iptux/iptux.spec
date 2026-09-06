# SPDX-License-Identifier: Apache-2.0
Name:           iptux
Version:        0.9.4
Release:        1%{?dist}
Summary:        A software for sharing in LAN
License:        GPL-2.0-or-later
URL:            https://github.com/iptux-src/iptux
Source0:        iptux-0.9.4.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A software for sharing in LAN

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
%license LICENSE
%doc README.md
%doc NEWS
%doc NEWS.md
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.4-1
- Initial openEuler RISC-V package from the full package inventory.
