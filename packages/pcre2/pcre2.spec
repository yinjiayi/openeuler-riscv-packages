# SPDX-License-Identifier: Apache-2.0
Name:           pcre2
Version:        10.48
Release:        2%{?dist}
Summary:        Perl-compatible regular expression library
License:        BSD-3-Clause WITH PCRE2-exception AND BSD-2-Clause
URL:            https://github.com/PCRE2Project/pcre2
Source0:        pcre2-10.48.tar.bz2

BuildRequires:  bzip2-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  readline-devel
BuildRequires:  zlib-devel

%description
PCRE2 is a set of libraries implementing regular-expression pattern matching
with a syntax and semantics closely modeled on Perl.

%package devel
Summary:        Development files for PCRE2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, manual pages, and unversioned links for all
supported PCRE2 code-unit widths.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-pcre2-16 \
  --enable-pcre2-32 \
  --enable-jit \
  --enable-unicode \
  --enable-pcre2grep-libz \
  --enable-pcre2grep-libbz2 \
  --enable-pcre2test-libreadline
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libpcre2-*.la

%check
%make_build check

%files
%license LICENCE.md deps/sljit/LICENSE
%doc AUTHORS.md ChangeLog NEWS README
%doc %{_docdir}/pcre2/
%{_bindir}/pcre2grep
%{_bindir}/pcre2test
%{_libdir}/libpcre2-8.so.0*
%{_libdir}/libpcre2-16.so.0*
%{_libdir}/libpcre2-32.so.0*
%{_libdir}/libpcre2-posix.so.3*
%{_mandir}/man1/pcre2grep.1*
%{_mandir}/man1/pcre2test.1*

%files devel
%license LICENCE.md deps/sljit/LICENSE
%{_bindir}/pcre2-config
%{_includedir}/pcre2.h
%{_includedir}/pcre2posix.h
%{_libdir}/libpcre2-8.so
%{_libdir}/libpcre2-16.so
%{_libdir}/libpcre2-32.so
%{_libdir}/libpcre2-posix.so
%{_libdir}/pkgconfig/libpcre2-8.pc
%{_libdir}/pkgconfig/libpcre2-16.pc
%{_libdir}/pkgconfig/libpcre2-32.pc
%{_libdir}/pkgconfig/libpcre2-posix.pc
%{_mandir}/man1/pcre2-config.1*
%{_mandir}/man3/pcre2*.3*

%changelog
* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 10.48-2
- Synchronize the installed smoke assertion and package documentation with 10.48.

* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 10.47-1
- Initial openEuler RISC-V package.
