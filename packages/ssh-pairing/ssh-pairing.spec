# SPDX-License-Identifier: Apache-2.0
Name:           ssh-pairing
Version:        0.4
Release:        1%{?dist}
Summary:        Passwordless SSH key exchange through pairing
License:        GPL-2.0-or-later
URL:            https://github.com/Vogtinator/ssh-pairing
Source0:        ssh-pairing-0.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Passwordless SSH key exchange through pairing

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4-1
- Initial openEuler RISC-V package from the full package inventory.
