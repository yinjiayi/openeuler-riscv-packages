# SPDX-License-Identifier: Apache-2.0
Name:           udns
Version:        0.6
Release:        1%{?dist}
Summary:        Asynchronous DNS stub resolver library
License:        LGPL-2.1-or-later
URL:            https://www.corpit.ru/mjt/udns.html
Source0:        udns-%{version}.tar.gz

BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  make

%description
udns is a small asynchronous DNS stub resolver library with synchronous
helpers and command-line query and DNS block-list utilities.

%package devel
Summary:        Development files for udns
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, static library, and unversioned linker name for developing software
with udns.

%prep
%autosetup -p1

%build
CC=%{__cc} CFLAGS='%{build_cflags}' LDFLAGS='%{build_ldflags}' \
  ./configure --enable-ipv6
%make_build static sharedlib

%install
install -Dpm 0755 dnsget %{buildroot}%{_bindir}/dnsget
install -Dpm 0755 rblcheck %{buildroot}%{_bindir}/rblcheck
install -Dpm 0644 libudns.so.0 %{buildroot}%{_libdir}/libudns.so.0
ln -s libudns.so.0 %{buildroot}%{_libdir}/libudns.so
install -Dpm 0644 libudns.a %{buildroot}%{_libdir}/libudns.a
install -Dpm 0644 udns.h %{buildroot}%{_includedir}/udns.h
install -Dpm 0644 dnsget.1 %{buildroot}%{_mandir}/man1/dnsget.1
install -Dpm 0644 rblcheck.1 %{buildroot}%{_mandir}/man1/rblcheck.1
install -Dpm 0644 udns.3 %{buildroot}%{_mandir}/man3/udns.3

%check
cat > version-check.c <<'EOF'
#include <stdio.h>
#include "udns.h"
int main(void) { puts(dns_version()); return 0; }
EOF
%{__cc} %{build_cflags} version-check.c ./libudns.so.0 -Wl,-rpath,. \
  %{build_ldflags} -o version-check
./version-check | grep -Fx '%{version}'

%files
%license COPYING.LGPL
%doc NEWS NOTES
%{_bindir}/dnsget
%{_bindir}/rblcheck
%{_libdir}/libudns.so.0
%{_mandir}/man1/dnsget.1*
%{_mandir}/man1/rblcheck.1*

%files devel
%license COPYING.LGPL
%{_includedir}/udns.h
%{_libdir}/libudns.a
%{_libdir}/libudns.so
%{_mandir}/man3/udns.3*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6-1
- Initial openEuler RISC-V package with an offline shared-library version probe.
