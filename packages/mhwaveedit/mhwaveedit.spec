# SPDX-License-Identifier: Apache-2.0
Name:           mhwaveedit
Version:        1.4.24
Release:        1%{?dist}
Summary:        A simple and fast GTK2 audio editor
License:        GPL-2.0-or-later
URL:            https://github.com/magnush/mhwaveedit
Source0:        mhwaveedit-1.4.24.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A simple and fast GTK2 audio editor

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
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.24-1
- Initial openEuler RISC-V package from the full package inventory.
