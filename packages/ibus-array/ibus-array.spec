# SPDX-License-Identifier: Apache-2.0
Name:           ibus-array
Version:        0.2.3
Release:        1%{?dist}
Summary:        The Array 30 input method for IBus input platform
License:        GPL-2.0-or-later
URL:            https://github.com/lexical/ibus-array
Source0:        ibus-array-0.2.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
The Array 30 input method for IBus input platform

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
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.3-1
- Initial openEuler RISC-V package from the full package inventory.
