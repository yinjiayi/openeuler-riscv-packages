# SPDX-License-Identifier: Apache-2.0
Name:           mistserver
Version:        3.11.1
Release:        1%{?dist}
Summary:        Internet streaming media toolkit
License:        Unlicense
URL:            https://github.com/DDVTECH/mistserver
Source0:        mistserver-3.11.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Internet streaming media toolkit

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
%license COPYING.md
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.11.1-1
- Initial openEuler RISC-V package from the full package inventory.
