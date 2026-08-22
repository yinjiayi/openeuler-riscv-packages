# SPDX-License-Identifier: Apache-2.0
Name:           attr
Version:        2.6.0
Release:        1%{?dist}
Summary:        Filesystem extended attribute utilities
License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://savannah.nongnu.org/projects/attr
Source0:        attr-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  perl
Requires:       libattr%{?_isa} = %{version}-%{release}

%description
The attr package provides attr, getfattr, and setfattr for inspecting and
changing extended attributes on filesystem objects.

%package -n libattr
Summary:        Runtime library for filesystem extended attributes
License:        LGPL-2.1-or-later

%description -n libattr
libattr provides compatibility interfaces for manipulating filesystem
extended attributes.

%package -n libattr-devel
Summary:        Development files for libattr
License:        LGPL-2.1-or-later
Requires:       libattr%{?_isa} = %{version}-%{release}
Requires:       glibc-headers

%description -n libattr-devel
Headers, pkg-config metadata, manual pages, and the unversioned library link
for developing applications with libattr.

%prep
%autosetup -p1

%build
%configure --disable-rpath --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libattr.a
rm -f %{buildroot}%{_libdir}/libattr.la
rm -rf %{buildroot}%{_docdir}/%{name}*
ln -s ../sys/xattr.h %{buildroot}%{_includedir}/attr/xattr.h
%find_lang %{name}

%check
export LD_LIBRARY_PATH="$PWD/libattr/.libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
%make_build check

%files -f %{name}.lang
%license doc/COPYING doc/COPYING.LGPL
%doc README doc/CHANGES
%{_bindir}/attr
%{_bindir}/getfattr
%{_bindir}/setfattr
%{_mandir}/man1/attr.1*
%{_mandir}/man1/getfattr.1*
%{_mandir}/man1/setfattr.1*

%files -n libattr
%license doc/COPYING.LGPL
%config(noreplace) %{_sysconfdir}/xattr.conf
%{_libdir}/libattr.so.1*

%files -n libattr-devel
%license doc/COPYING.LGPL
%{_includedir}/attr/
%{_libdir}/libattr.so
%{_libdir}/pkgconfig/libattr.pc
%{_mandir}/man3/attr_*.3*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.0-1
- Initial openEuler RISC-V package with the complete upstream test suite.
