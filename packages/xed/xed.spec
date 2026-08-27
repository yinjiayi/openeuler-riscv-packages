# SPDX-License-Identifier: Apache-2.0
Name:           xed
Version:        3.8.9
Release:        1%{?dist}
Summary:        A small and lightweight text editor
License:        GPL-2.0-or-later
URL:            https://github.com/linuxmint/xed
Source0:        xed-3.8.9.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A small and lightweight text editor

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
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.8.9-1
- Initial openEuler RISC-V package from the full package inventory.
