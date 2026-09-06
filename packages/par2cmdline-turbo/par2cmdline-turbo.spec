# SPDX-License-Identifier: Apache-2.0
Name:           par2cmdline-turbo
Version:        1.4.0
Release:        1%{?dist}
Summary:        A faster PAR 2.0 compatible file verification and repair tool, forked from par2cmdline
License:        GPL-2.0-or-later
URL:            https://github.com/animetosho/par2cmdline-turbo
Source0:        par2cmdline-turbo-1.4.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
A faster PAR 2.0 compatible file verification and repair tool, forked from par2cmdline

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
