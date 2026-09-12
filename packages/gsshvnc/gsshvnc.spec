# SPDX-License-Identifier: Apache-2.0
Name:           gsshvnc
Version:        0.96
Release:        1%{?dist}
Summary:        A simple VNC client with built-in SSH tunneling
License:        GPL-2.0-or-later
URL:            https://github.com/zrax/gsshvnc
Source0:        gsshvnc-0.96.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A simple VNC client with built-in SSH tunneling

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

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.96-1
- Initial openEuler RISC-V package from the full package inventory.
