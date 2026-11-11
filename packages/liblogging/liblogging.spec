# SPDX-License-Identifier: Apache-2.0
Name:           liblogging
Version:        1.0.6
Release:        1%{?dist}
Summary:        Portable library for system logging
License:        BSD-2-Clause AND Apache-2.0
URL:            https://liblogging.org/
Source0:        liblogging-%{version}.tar.gz
Patch0:         0001-declare-frame-body-return.patch
Patch1:         0002-declare-unix-domain-socket-init.patch
Patch2:         0003-add-original-tester-replay.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  python3-docutils
BuildRequires:  systemd-devel
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  grep

%description
liblogging provides a portable standard logging API with file, syslog,
Unix-domain socket, systemd journal, and RFC 3195 output support.

%package devel
Summary:        Development files for liblogging
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, original-default static archives, pkg-config metadata, and
unversioned shared-library links for developing applications with liblogging.

%package tests
Summary:        Original source-only liblogging tester and replay driver
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       bash
Requires:       gcc
Requires:       binutils
Requires:       pkgconf
Requires:       systemd-devel
Requires:       coreutils
Requires:       grep
Requires:       rpm

%description tests
The unmodified released stdlog tester source, complete license, and an offline
driver to compile and replay it against staged or installed shared and static
libraries. No test binary is distributed. File output is tested; this does not
claim native systemd service, networking, timing, or hardware validation.

%prep
%autosetup -p1

%build
autoreconf -fiv
%configure \
  --enable-journal \
  --enable-rfc3195 \
  --enable-stdlog
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
install -d %{buildroot}%{_datadir}/liblogging/qa
install -m 0644 stdlog/tester.c COPYING downstream/QA-LICENSE %{buildroot}%{_datadir}/liblogging/qa/
install -m 0755 downstream/run-tests.sh %{buildroot}%{_datadir}/liblogging/qa/
(cd %{buildroot}%{_datadir}/liblogging/qa && sha256sum tester.c COPYING QA-LICENSE run-tests.sh > SHA256SUMS)

%check
%make_build check
./stdlog/tester 'file:liblogging-test.log'
test -s liblogging-test.log
bash downstream/run-tests.sh "%{buildroot}" "%{_libdir}"

%files
%license COPYING downstream/QA-LICENSE
%doc ChangeLog README.md
%{_bindir}/stdlogctl
%{_libdir}/liblogging-rfc3195.so.0*
%{_libdir}/liblogging-stdlog.so.0*
%{_mandir}/man1/stdlogctl.1*
%{_mandir}/man3/stdlog.3*

%files devel
%license COPYING downstream/QA-LICENSE
%{_includedir}/liblogging/
%{_libdir}/liblogging-rfc3195.so
%{_libdir}/liblogging-stdlog.so
%{_libdir}/liblogging-rfc3195.a
%{_libdir}/liblogging-stdlog.a
%{_libdir}/pkgconfig/liblogging-rfc3195.pc
%{_libdir}/pkgconfig/liblogging-stdlog.pc

%files tests
%license COPYING downstream/QA-LICENSE
%{_datadir}/liblogging/

%changelog
* Sun Oct 18 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.6-1
- Retain declaration patches, restore static defaults and replay original installed tester.
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.6-1
- Initial openEuler RISC-V package from the full package inventory.
