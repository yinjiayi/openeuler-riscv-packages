# SPDX-License-Identifier: Apache-2.0
Name:           fakechroot
Version:        2.20.1
Release:        1%{?dist}
Summary:        gives a fake chroot environment
License:        LGPL-2.1-or-later
URL:            https://github.com/dex4er/fakechroot
Source0:        fakechroot-2.20.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
gives a fake chroot environment

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%license LICENSE
%doc README.md
%doc NEWS.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.20.1-1
- Initial openEuler RISC-V package from the full package inventory.
