# SPDX-License-Identifier: Apache-2.0
Name:           tnef
Version:        1.4.18
Release:        1%{?dist}
Summary:        Program for unpacking ms-tnef MIME attachment
License:        GPL-2.0-or-later
URL:            https://github.com/verdammelt/tnef
Source0:        tnef-1.4.18.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Program for unpacking ms-tnef MIME attachment

%prep
%autosetup -p1

%build
autoreconf -fi
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
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.18-1
- Initial openEuler RISC-V package from the full package inventory.
