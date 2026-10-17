# SPDX-License-Identifier: Apache-2.0
Name:           liblogging
Version:        1.0.6
Release:        1%{?dist}
Summary:        Portable library for system logging
License:        BSD-2-Clause
URL:            https://liblogging.org/
Source0:        liblogging-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  python3-docutils
BuildRequires:  systemd-devel

%description
liblogging provides a portable standard logging API with file, syslog,
Unix-domain socket, systemd journal, and RFC 3195 output support.

%package devel
Summary:        Development files for liblogging
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and unversioned shared-library links for
developing applications with liblogging.

%prep
%autosetup -p1
# GCC 14 no longer accepts the implicit int used by this old RFC 3195 helper.
sed -i '/^sbFramActualRecvFramCommonBody/i int' rfc3195/src/beepframe.c
# The Unix-domain socket implementation is public to beeplisten.c but the
# released header omits its prototype, which GCC 14 rejects.
sed -i '/^srRetVal sbSock_gethostname/i srRetVal sbSock_InitUXDOMSOCK(sbSockObj **ppThis, char *pszSockName, int iSockType);' rfc3195/src/sockets.h

%build
autoreconf -fiv
%configure \
  --disable-static \
  --enable-journal \
  --enable-rfc3195 \
  --enable-stdlog
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check
./stdlog/tester 'file:liblogging-test.log'
test -s liblogging-test.log

%files
%license COPYING
%doc ChangeLog README.md
%{_bindir}/stdlogctl
%{_libdir}/liblogging-rfc3195.so.0*
%{_libdir}/liblogging-stdlog.so.0*
%{_mandir}/man1/stdlogctl.1*
%{_mandir}/man3/stdlog.3*

%files devel
%license COPYING
%{_includedir}/liblogging/
%{_libdir}/liblogging-rfc3195.so
%{_libdir}/liblogging-stdlog.so
%{_libdir}/pkgconfig/liblogging-rfc3195.pc
%{_libdir}/pkgconfig/liblogging-stdlog.pc

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.6-1
- Initial openEuler RISC-V package from the full package inventory.
