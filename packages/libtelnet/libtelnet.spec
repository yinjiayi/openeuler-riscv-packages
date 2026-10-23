# SPDX-License-Identifier: Apache-2.0
Name:           libtelnet
Version:        0.23
Release:        1%{?dist}
Summary:        TELNET protocol parsing and negotiation library
License:        LicenseRef-libtelnet-public-domain AND Zlib
URL:            https://github.com/seanmiddleditch/libtelnet
Source0:        libtelnet-0.23.tar.gz
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  doxygen
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  sed
BuildRequires:  zlib-devel
Requires:       bash
Requires:       coreutils
Requires:       diffutils
Requires:       grep
Requires:       sed
Requires:       zlib

%description
Callback-oriented TELNET protocol parsing, negotiation and formatting library,
including the upstream command-line utilities and offline parser regression data.

%prep
%autosetup -p1

%build
%configure
%make_build
# Build the default check program without executing upstream source locally.
%make_build -C util telnet-test

%install
%make_install
rm -f %{buildroot}%{_libdir}/libtelnet.la
install -d %{buildroot}%{_libexecdir}/libtelnet-tests
install -m 0755 util/.libs/telnet-test %{buildroot}%{_libexecdir}/libtelnet-tests/telnet-test
install -d %{buildroot}%{_datadir}/libtelnet/test
install -m 0755 test/run-all.sh test/run-test.sh %{buildroot}%{_datadir}/libtelnet/test/
install -m 0644 test/*.test %{buildroot}%{_datadir}/libtelnet/test/
(cd %{buildroot}%{_datadir}/libtelnet && sha256sum test/* > tests.sha256)

%check
%make_build check
# Automake registers one shell suite; that unchanged suite compares all 11 fixtures.
test "$(grep -c 'OK$' test/run-all.sh.log)" -eq 11
! grep -q 'FAIL' test/run-all.sh.log

%files
%license COPYING msvc2008/zlib.h
%doc NEWS AUTHORS ChangeLog
%{_bindir}/telnet-client
%{_bindir}/telnet-chatd
%{_bindir}/telnet-proxy
%{_libdir}/libtelnet.so*
%{_libdir}/libtelnet.a
%{_libdir}/pkgconfig/libtelnet.pc
%{_includedir}/libtelnet.h
%{_mandir}/man1/telnet-client.1*
%{_mandir}/man1/telnet-chatd.1*
%{_mandir}/man1/telnet-proxy.1*
%{_mandir}/man3/*.3*
%{_libexecdir}/libtelnet-tests/
%{_datadir}/libtelnet/

%changelog
* Thu Jan 01 1970 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.23-1
- Package the official stable release, default utilities, documentation and tests.
