# SPDX-License-Identifier: Apache-2.0
Name:           budgie-session
Version:        1.0.1
Release:        1%{?dist}
Summary:        The Budgie Desktop session handler
License:        GPL-2.0-or-later
URL:            https://github.com/BuddiesOfBudgie/budgie-session
Source0:        budgie-session-1.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
The Budgie Desktop session handler

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
