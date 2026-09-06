# SPDX-License-Identifier: Apache-2.0
Name:           dovecot-fts-xapian
Version:        1.9.3
Release:        1%{?dist}
Summary:        Dovecot FTS plugin based on Xapian
License:        LGPL-2.1-or-later
URL:            https://github.com/grosjo/fts-xapian
Source0:        dovecot-fts-xapian-1.9.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Dovecot FTS plugin based on Xapian

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.3-1
- Initial openEuler RISC-V package from the full package inventory.
