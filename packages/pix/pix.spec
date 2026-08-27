# SPDX-License-Identifier: Apache-2.0
Name:           pix
Version:        3.4.10
Release:        1%{?dist}
Summary:        Image viewer and browser based on gthumb. X-Apps Project.
License:        GPL-2.0-or-later
URL:            https://github.com/linuxmint/pix
Source0:        pix-3.4.10.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Image viewer and browser based on gthumb. X-Apps Project.

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

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.4.10-1
- Initial openEuler RISC-V package from the full package inventory.
