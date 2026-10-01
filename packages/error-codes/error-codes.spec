# SPDX-License-Identifier: Apache-2.0
Name:           error-codes
Version:        0.4.0
Release:        1%{?dist}
Summary:        Lookup error codes and their description
License:        GPL-2.0-or-later
URL:            https://github.com/thkukuk/error-codes
Source0:        error-codes-0.4.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Lookup error codes and their description

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
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
