# SPDX-License-Identifier: Apache-2.0
Name:           tgt
Version:        1.0.97
Release:        1%{?dist}
Summary:        iSCSI Target STGT for Arch Linux
License:        GPL-2.0-or-later
URL:            https://github.com/fujita/tgt
Source0:        tgt-1.0.97.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
iSCSI Target STGT for Arch Linux

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.97-1
- Initial openEuler RISC-V package from the full package inventory.
