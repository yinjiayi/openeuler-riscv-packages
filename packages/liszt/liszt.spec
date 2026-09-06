# SPDX-License-Identifier: Apache-2.0
Name:           liszt
Version:        0.3.0
Release:        1%{?dist}
Summary:        GNU ls reimplementation: byte-identical output, radix sorts, parallel stat
License:        GPL-3.0-or-later
URL:            https://github.com/tenseleyFlow/liszt
Source0:        liszt-0.3.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
GNU ls reimplementation: byte-identical output, radix sorts, parallel stat

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
