# SPDX-License-Identifier: Apache-2.0
Name:           pqiv
Version:        2.13.3
Release:        1%{?dist}
Summary:        Powerful image viewer with minimal UI
License:        GPL-3.0-or-later
URL:            https://github.com/phillipberndt/pqiv
Source0:        pqiv-2.13.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Powerful image viewer with minimal UI

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


%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.13.3-1
- Initial openEuler RISC-V package from the full package inventory.
