# SPDX-License-Identifier: Apache-2.0
Name:           faac
Version:        2.0
Release:        1%{?dist}
Summary:        Freeware Advanced Audio Coder
License:        LGPL-2.1-or-later
URL:            https://github.com/knik0/faac
Source0:        faac-2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Freeware Advanced Audio Coder

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0-1
- Initial openEuler RISC-V package from the full package inventory.
