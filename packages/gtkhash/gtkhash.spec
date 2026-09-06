# SPDX-License-Identifier: Apache-2.0
Name:           gtkhash
Version:        1.5
Release:        1%{?dist}
Summary:        A GTK+ utility for computing message digests or checksums
License:        GPL-2.0-or-later
URL:            https://github.com/tristanheaven/gtkhash
Source0:        gtkhash-1.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A GTK+ utility for computing message digests or checksums

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5-1
- Initial openEuler RISC-V package from the full package inventory.
