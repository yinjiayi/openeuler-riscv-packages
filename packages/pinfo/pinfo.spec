# SPDX-License-Identifier: Apache-2.0
Name:           pinfo
Version:        0.6.13
Release:        1%{?dist}
Summary:        A hypertext info file viewer
License:        GPL-2.0-or-later
URL:            https://github.com/baszoetekouw/pinfo
Source0:        pinfo-0.6.13.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A hypertext info file viewer

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.13-1
- Initial openEuler RISC-V package from the full package inventory.
