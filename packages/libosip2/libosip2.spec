# SPDX-License-Identifier: Apache-2.0
Name:           libosip2
Version:        5.3.2
Release:        1%{?dist}
Summary:        GNU oSIP library for SIP message parsing and transactions
License:        LGPL-2.1-or-later
URL:            https://www.gnu.org/software/osip/
Source0:        libosip2-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
GNU oSIP provides SIP message parsing and transaction state machines for
applications using the Session Initiation Protocol.

%package devel
Summary:        Development files for libosip2
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Public headers, linker names, pkg-config metadata, and the manual page for
applications using GNU oSIP.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-mt --enable-test
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# Upstream's fixture driver prints failure counts but returns zero even when
# torture_test fails. Preserve all registered tests and enforce their counts.
%make_build check > osip-check.log 2>&1 || {
  cat osip-check.log
  exit 1
}
cat osip-check.log
awk '
  /^unit testing total[[:space:]]*:/ { total = $NF; has_total = 1 }
  /^unit testing passed:/ { passed = $NF; has_passed = 1 }
  /^unit testing failed:/ { failed = $NF; has_failed = 1 }
  END {
    if (!has_total || !has_passed || !has_failed || total < 120 ||
        passed != total || failed != 0) exit 1
  }
' osip-check.log

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libosip2.so.15*
%{_libdir}/libosipparser2.so.15*

%files devel
%license COPYING
%{_includedir}/osip2/
%{_includedir}/osipparser2/
%{_libdir}/libosip2.so
%{_libdir}/libosipparser2.so
%{_libdir}/pkgconfig/libosip2.pc
%{_mandir}/man1/osip.1*

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.3.2-1
- Initial openEuler RISC-V package with enforced upstream SIP fixture tests.
