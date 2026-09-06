# SPDX-License-Identifier: Apache-2.0
Name:           waytator
Version:        1.2.4
Release:        1%{?dist}
Summary:        Screenshot annotator and lightweight image editor
License:        GPL-3.0-or-later
URL:            https://github.com/faetalize/waytator
Source0:        waytator-1.2.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Screenshot annotator and lightweight image editor

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.4-1
- Initial openEuler RISC-V package from the full package inventory.
