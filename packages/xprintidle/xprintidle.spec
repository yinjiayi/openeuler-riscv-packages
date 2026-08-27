# SPDX-License-Identifier: Apache-2.0
Name:           xprintidle
Version:        0.3.0
Release:        1%{?dist}
Summary:        Print the X server user idle time
License:        GPL-2.0-or-later
URL:            https://github.com/g0hl1n/xprintidle
Source0:        xprintidle-0.3.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Print the X server user idle time

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
