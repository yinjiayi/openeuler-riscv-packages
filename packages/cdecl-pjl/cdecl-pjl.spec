# SPDX-License-Identifier: Apache-2.0
Name:           cdecl-pjl
Version:        18.7.2
Release:        1%{?dist}
Summary:        C declaration converter with improvements by Paul J. Lucas
License:        GPL-3.0-or-later
URL:            https://github.com/paul-j-lucas/cdecl
Source0:        cdecl-pjl-18.7.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
C declaration converter with improvements by Paul J. Lucas

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 18.7.2-1
- Initial openEuler RISC-V package from the full package inventory.
