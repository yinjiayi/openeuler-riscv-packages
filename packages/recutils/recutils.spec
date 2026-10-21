# SPDX-License-Identifier: Apache-2.0
Name:           recutils
Version:        1.9
Release:        1%{?dist}
Summary:        Tools and library for text-based recfile databases
License:        GPL-3.0-or-later AND GFDL-1.3-or-later
URL:            https://www.gnu.org/software/recutils/
Source0:        recutils-%{version}.tar.gz
Patch0:         0001-fix-generated-lexer-declarations.patch
Patch1:         0002-fix-bash-builtin-argv-type.patch
Patch2:         0003-fix-torture-missing-stdlib.patch

BuildRequires:  bash-devel
BuildRequires:  bison
BuildRequires:  check-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  help2man
BuildRequires:  libcurl-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  readline-devel
BuildRequires:  texinfo
BuildRequires:  uuid-devel
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
GNU recutils is a set of command-line tools for creating, querying, editing,
and converting human-readable text databases called recfiles.

%package libs
Summary:        Runtime library for GNU recutils

%description libs
The shared librec library used by GNU recutils and applications that process
recfiles.

%package devel
Summary:        Development files for GNU recutils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The public header and unversioned linker name for developing applications
with librec.

%package bash-builtins
Summary:        GNU recutils loadable builtins for Bash
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       bash

%description bash-builtins
The readrec and testrec loadable Bash builtins for reading and testing
recfiles from shell scripts.

%prep
%autosetup -p1

%build
%configure \
  --disable-rpath \
  --disable-static \
  --enable-bash-builtins \
  --enable-encryption \
  --with-bash-headers=%{_includedir}/bash
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir
%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/csv2rec
%{_bindir}/rec2csv
%{_bindir}/recdel
%{_bindir}/recfix
%{_bindir}/recfmt
%{_bindir}/recinf
%{_bindir}/recins
%{_bindir}/recsel
%{_bindir}/recset
%{_datadir}/%{name}/
%{_infodir}/recutils.info*
%{_mandir}/man1/csv2rec.1*
%{_mandir}/man1/rec2csv.1*
%{_mandir}/man1/recdel.1*
%{_mandir}/man1/recfix.1*
%{_mandir}/man1/recfmt.1*
%{_mandir}/man1/recinf.1*
%{_mandir}/man1/recins.1*
%{_mandir}/man1/recsel.1*
%{_mandir}/man1/recset.1*

%files libs
%license COPYING
%{_libdir}/librec.so.1*

%files devel
%license COPYING
%{_includedir}/rec.h
%{_libdir}/librec.so

%files bash-builtins
%license COPYING
%{_libdir}/readrec.so*
%{_libdir}/testrec.so*

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9-1
- Initial openEuler RISC-V package from official GNU and frozen distribution evidence.
- Apply the upstream-submitted generated lexer declaration fix for strict C99 builds.
- Match Bash 5.2's make_builtin_argv return type in the testrec builtin.
- Apply the accepted upstream torture include fix for strict C compilation.
- Package the complete libtool output for both loadable Bash builtins.
