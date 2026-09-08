# SPDX-License-Identifier: Apache-2.0
Name:           libedit
Version:        20260512.3.1
Release:        1%{?dist}
Summary:        BSD line-editing, history, and tokenization library
License:        BSD-3-Clause AND BSD-2-Clause AND ISC
URL:            https://www.thrysoee.dk/editline/
Source0:        libedit-20260512-3.1.tar.gz

BuildRequires:  gcc
BuildRequires:  groff-base
BuildRequires:  make
BuildRequires:  ncurses-devel

%description
Libedit is an autotools port of the NetBSD Editline library. It provides line
editing, history, and tokenization interfaces similar to GNU Readline.

%package devel
Summary:        Development files for libedit
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ncurses-devel%{?_isa}

%description devel
Headers, pkg-config metadata, examples, manual pages, and the unversioned
library link for developing applications with libedit.

%prep
%autosetup -n libedit-20260512-3.1 -p1

%build
%configure --disable-silent-rules --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libedit.la

%check
%make_build check

%files
%license COPYING
%doc ChangeLog THANKS
%{_libdir}/libedit.so.0*
%{_mandir}/man5/editrc.5*

%files devel
%license COPYING
%doc examples/fileman.c examples/tc1.c examples/wtc1.c
%{_includedir}/histedit.h
%{_includedir}/editline/
%{_libdir}/libedit.so
%{_libdir}/pkgconfig/libedit.pc
%{_mandir}/man3/*.3*
%{_mandir}/man7/editline.7*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 20260512.3.1-1
- Initial openEuler RISC-V package with the upstream check target.
