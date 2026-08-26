# SPDX-License-Identifier: Apache-2.0
Name:           snoopy-logger
Version:        2.5.2
Release:        1%{?dist}
Summary:        A small library that logs all program executions
License:        GPL-2.0-or-later
URL:            https://github.com/a2o/snoopy
Source0:        snoopy-logger-2.5.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A small library that logs all program executions

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README.md
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.2-1
- Initial openEuler RISC-V package from the full package inventory.
