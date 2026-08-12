# SPDX-License-Identifier: Apache-2.0
Name:           dos2unix
Version:        7.5.6
Release:        1%{?dist}
Summary:        DOS, Unix, and Mac text file format converters
License:        BSD-3-Clause
URL:            https://waterlander.net/dos2unix/
Source0:        dos2unix-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple

%description
Dos2unix converts text files between DOS, Unix, and classic Mac line endings,
with Unicode, byte-order-mark, safe in-place, and standard-stream support.

%prep
%autosetup -p1

%build
%make_build prefix=%{_prefix} CFLAGS_USER="%{optflags}" LDFLAGS_USER="%{build_ldflags}"

%install
%make_install prefix=%{_prefix}
%find_lang %{name} --with-man

%check
%make_build test

%files -f %{name}.lang
%license COPYING.txt
%doc BUGS.txt ChangeLog.txt NEWS.txt README.txt TODO.txt
%{_bindir}/dos2unix
%{_bindir}/mac2unix
%{_bindir}/unix2dos
%{_bindir}/unix2mac
%{_mandir}/man1/*.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.5.6-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
