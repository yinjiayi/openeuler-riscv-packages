# SPDX-License-Identifier: Apache-2.0
Name:           gdbm
Epoch:          1
Version:        1.26
Release:        1%{?dist}
Summary:        GNU database library and command-line tools
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gdbm/
Source0:        gdbm-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  readline-devel
BuildRequires:  texinfo
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description
GDBM is GNU's library of persistent key-value database routines. This package
contains the gdbm_dump, gdbm_load, gdbm_recover, and gdbmtool utilities.

%package libs
Summary:        Runtime libraries for GDBM

%description libs
The GDBM and ndbm compatibility shared libraries.

%package devel
Summary:        Development files for GDBM
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
Headers, manual pages, Info documentation, and unversioned library links for
developing applications with GDBM.

%prep
%autosetup -p1

%build
%configure \
  --disable-rpath \
  --disable-static \
  --enable-libgdbm-compat
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir
mkdir -p %{buildroot}%{_includedir}/gdbm
ln -s ../gdbm.h %{buildroot}%{_includedir}/gdbm/gdbm.h
ln -s ../ndbm.h %{buildroot}%{_includedir}/gdbm/ndbm.h
ln -s ../dbm.h %{buildroot}%{_includedir}/gdbm/dbm.h
%find_lang %{name}

%check
export LD_LIBRARY_PATH="$PWD/src/.libs:$PWD/compat/.libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS NOTE-WARNING README THANKS
%{_bindir}/gdbm*
%{_mandir}/man1/gdbm*.1*

%files libs
%license COPYING
%{_libdir}/libgdbm.so.6*
%{_libdir}/libgdbm_compat.so.4*

%files devel
%license COPYING
%{_includedir}/dbm.h
%{_includedir}/gdbm.h
%{_includedir}/ndbm.h
%{_includedir}/gdbm/
%{_libdir}/libgdbm.so
%{_libdir}/libgdbm_compat.so
%{_infodir}/gdbm.info*
%{_mandir}/man3/*.3*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1:1.26-1
- Initial openEuler RISC-V package with GDBM and compatibility tests.
