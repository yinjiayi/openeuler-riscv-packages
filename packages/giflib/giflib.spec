# SPDX-License-Identifier: Apache-2.0
Name:           giflib
Version:        6.1.3
Release:        1%{?dist}
Summary:        Library and utilities for reading and writing GIF images
License:        MIT
URL:            https://giflib.sourceforge.net/
Source0:        giflib-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
giflib is a library for reading and writing GIF images. This package also
contains command-line tools for inspecting, repairing, and generating GIFs.

%package devel
Summary:        Development files for giflib
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and unversioned shared-library link for developing applications with
giflib.

%prep
%autosetup -p1

%build
%make_build \
  CFLAGS="%{optflags} -std=gnu99 -fPIC -Wall" \
  LDFLAGS="%{build_ldflags}"

%install
%make_install \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  MANDIR=%{_mandir} \
  DOCDIR=%{_docdir}/%{name}
find %{buildroot} -name '*.a' -delete

%check
%make_build check \
  CFLAGS="%{optflags} -std=gnu99 -fPIC -Wall" \
  LDFLAGS="%{build_ldflags}"

%files
%license COPYING
%doc ChangeLog NEWS README.adoc
%{_bindir}/gifbuild
%{_bindir}/gifclrmp
%{_bindir}/giffix
%{_bindir}/giftext
%{_bindir}/giftool
%{_docdir}/%{name}/html/
%{_libdir}/libgif.so.7*
%{_mandir}/man1/gifbuild.1*
%{_mandir}/man1/gifclrmp.1*
%{_mandir}/man1/giffix.1*
%{_mandir}/man1/giftext.1*
%{_mandir}/man1/giftool.1*
%{_mandir}/man7/giflib.7*

%files devel
%license COPYING
%{_includedir}/gif_lib.h
%{_libdir}/libgif.so

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.1.3-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
