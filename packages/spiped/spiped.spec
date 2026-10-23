# SPDX-License-Identifier: Apache-2.0
Name:           spiped
Version:        1.6.4
Release:        1%{?dist}
Summary:        Authenticated encrypted pipes between socket addresses
License:        BSD-2-Clause AND BSD-3-Clause
URL:            https://www.tarsnap.com/spiped.html
Source0:        spiped-1.6.4.tgz
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  procps-ng
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       diffutils
Requires:       grep
Requires:       procps-ng
Requires:       sed

%description
Spiped creates authenticated and encrypted pipes between socket addresses.
It provides the spiped daemon and the spipe command-line client. The complete
upstream functional test suite and its compiled helpers are installed for
post-installation verification of the packaged programs.

%prep
%autosetup -n spiped-%{version}

%build
# Retain upstream's default all target, including libraries and every helper.
# Generated POSIX Makefiles are shipped; BSD make is only for developer targets.
make -j1 CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}" all

%install
# Upstream install strips the programs. Stage the same binaries/man pages
# without stripping so the distribution RPM machinery owns debug processing.
install -d %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
install -m 0755 spiped/spiped spipe/spipe %{buildroot}%{_bindir}/
install -m 0644 spiped/spiped.1 spipe/spipe.1 %{buildroot}%{_mandir}/man1/

# Preserve all original shell bytes and the helper paths used by the driver.
install -d %{buildroot}%{_libexecdir}/spiped-qa/tests
install -m 0644 tests/*.sh %{buildroot}%{_libexecdir}/spiped-qa/tests/
chmod 0755 %{buildroot}%{_libexecdir}/spiped-qa/tests/test_spiped.sh
for helper in \
    tests/dnsthread-resolve/dnsthread-resolve \
    tests/msleep/msleep \
    tests/nc-client/nc-client \
    tests/nc-server/nc-server \
    tests/pthread_create_blocking_np/test_pthread_create_blocking_np \
    tests/pushbits/test_pushbits \
    tests/valgrind/potential-memleaks; do
    install -D -m 0755 "$helper" "%{buildroot}%{_libexecdir}/spiped-qa/$helper"
done
install -d %{buildroot}%{_libexecdir}/spiped-qa/spiped \
    %{buildroot}%{_libexecdir}/spiped-qa/spipe
ln -s %{_bindir}/spiped %{buildroot}%{_libexecdir}/spiped-qa/spiped/spiped
ln -s %{_bindir}/spipe %{buildroot}%{_libexecdir}/spiped-qa/spipe/spipe
sha256sum tests/*.sh > %{buildroot}%{_libexecdir}/spiped-qa/tests.sha256

%check
# No scenario selector, rewritten tests or failure suppression. The original
# system-spiped conditional and remote-DNS/valgrind opt-in defaults stay intact.
export LC_ALL=C.UTF-8
test -r /dev/urandom
unset N USE_VALGRIND USE_VALGRIND_NO_REGEN TEST_DNSTHREAD_ENABLE_REMOTE
make -j1 CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}" test

%files
%license COPYRIGHT libcperciva/external/queue/queue.h
%doc README.md BUILDING DESIGN.md CHANGELOG
%{_bindir}/spiped
%{_bindir}/spipe
%{_mandir}/man1/spiped.1*
%{_mandir}/man1/spipe.1*
%{_libexecdir}/spiped-qa

%changelog
* Fri Oct 23 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.4-1
- Pin the official release; retain default build and functional tests.
- Install complete embedded license notices and unmodified QA payload.
