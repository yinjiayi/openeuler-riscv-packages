# SPDX-License-Identifier: Apache-2.0
Name:           deepin-pw-check
Version:        6.0.12
Release:        1%{?dist}
Summary:        Tool to verify the validity of the password
License:        GPL-2.0-or-later
URL:            https://github.com/linuxdeepin/deepin-pw-check
Source0:        deepin-pw-check-6.0.12.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Tool to verify the validity of the password

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.12-1
- Initial openEuler RISC-V package from the full package inventory.
