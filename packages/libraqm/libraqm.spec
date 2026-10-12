# SPDX-License-Identifier: Apache-2.0
Name:           libraqm
Version:        0.11.0
Release:        1%{?dist}
Summary:        A library that encapsulates the logic for complex text layout
License:        MIT
URL:            https://github.com/HOST-Oman/libraqm
Source0:        libraqm-0.11.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A library that encapsulates the logic for complex text layout

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11.0-1
- Initial openEuler RISC-V package from the full package inventory.
