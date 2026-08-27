# SPDX-License-Identifier: Apache-2.0
Name:           sysbench
Version:        1.0.20
Release:        1%{?dist}
Summary:        Scriptable multi-threaded benchmark tool for databases and systems
License:        GPL-2.0-or-later
URL:            https://github.com/akopytov/sysbench
Source0:        sysbench-1.0.20.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Scriptable multi-threaded benchmark tool for databases and systems

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
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.20-1
- Initial openEuler RISC-V package from the full package inventory.
