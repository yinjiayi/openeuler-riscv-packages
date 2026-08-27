# SPDX-License-Identifier: Apache-2.0
Name:           isomd5sum
Version:        1.2.5
Release:        1%{?dist}
Summary:        Utilities for working with md5sum implanted in ISO images
License:        GPL-2.0-or-later
URL:            https://github.com/rhinstaller/isomd5sum
Source0:        isomd5sum-1.2.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Utilities for working with md5sum implanted in ISO images

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
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.5-1
- Initial openEuler RISC-V package from the full package inventory.
