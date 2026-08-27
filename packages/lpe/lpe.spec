# SPDX-License-Identifier: Apache-2.0
Name:           lpe
Version:        1.2.8
Release:        1%{?dist}
Summary:        Programming text editor
License:        GPL-2.0-or-later
URL:            https://github.com/AdamMajer/lpe
Source0:        lpe-1.2.8.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Programming text editor

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
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.8-1
- Initial openEuler RISC-V package from the full package inventory.
