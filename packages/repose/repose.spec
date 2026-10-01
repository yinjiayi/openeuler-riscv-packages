# SPDX-License-Identifier: Apache-2.0
Name:           repose
Version:        7.1
Release:        1%{?dist}
Summary:        Arch Linux repo building tool
License:        GPL-2.0-or-later
URL:            https://github.com/vodik/repose
Source0:        repose-7.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Arch Linux repo building tool

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
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.1-1
- Initial openEuler RISC-V package from the full package inventory.
