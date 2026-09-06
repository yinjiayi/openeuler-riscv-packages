# SPDX-License-Identifier: Apache-2.0
Name:           pam-luks-keyring-unlock
Version:        1.0.1
Release:        1%{?dist}
Summary:        A PAM module that seamlessly unlocks your Gnome Keyring and KDE Wallet using your LUKS encryption key.
License:        MIT
URL:            https://github.com/cubic3d/pam-luks-keyring-unlock
Source0:        pam-luks-keyring-unlock-1.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A PAM module that seamlessly unlocks your Gnome Keyring and KDE Wallet using your LUKS encryption key.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
