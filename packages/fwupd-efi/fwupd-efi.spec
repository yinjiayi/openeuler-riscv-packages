# SPDX-License-Identifier: Apache-2.0
Name:           fwupd-efi
Version:        1.8
Release:        1%{?dist}
Summary:        EFI Application used by uefi-capsule plugin in fwupd
License:        LGPL-2.1-or-later
URL:            https://github.com/fwupd/fwupd-efi
Source0:        fwupd-efi-1.8.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
EFI Application used by uefi-capsule plugin in fwupd

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8-1
- Initial openEuler RISC-V package from the full package inventory.
