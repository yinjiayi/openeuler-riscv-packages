# SPDX-License-Identifier: Apache-2.0
Name:           gavl
Version:        2.0.1
Release:        1%{?dist}
Summary:        Low level library, upon which multimedia APIs can be built
License:        GPL-2.0-or-later
URL:            https://github.com/bplaum/gavl
Source0:        gavl-2.0.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Low level library, upon which multimedia APIs can be built

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
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
