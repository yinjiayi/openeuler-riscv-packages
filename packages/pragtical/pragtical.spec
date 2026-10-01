# SPDX-License-Identifier: Apache-2.0
Name:           pragtical
Version:        3.12.4
Release:        1%{?dist}
Summary:        The practical and pragmatic code editor.
License:        MIT
URL:            https://github.com/pragtical/pragtical
Source0:        pragtical-3.12.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
The practical and pragmatic code editor.

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

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.12.4-1
- Initial openEuler RISC-V package from the full package inventory.
