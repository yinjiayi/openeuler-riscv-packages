# SPDX-License-Identifier: Apache-2.0
Name:           libaio
Version:        0.3.113
Release:        1%{?dist}
Summary:        Linux native asynchronous I/O library
License:        LGPL-2.1-or-later
URL:            https://pagure.io/libaio
Source0:        libaio-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
libaio provides userspace access to the Linux kernel asynchronous I/O system
calls.

%package devel
Summary:        Development files for libaio
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The libaio header, manual pages, and unversioned library link for developing
applications that use Linux native asynchronous I/O.

%prep
%autosetup -p1

%build
CFLAGS="%{optflags}" \
  LDFLAGS="%{__global_ldflags}" \
%make_build \
  libdir=%{_libdir}

%install
%{__make} install \
  DESTDIR=%{buildroot} \
  prefix=%{_prefix} \
  includedir=%{_includedir} \
  libdir=%{_libdir}
rm -f %{buildroot}%{_libdir}/libaio.a
%{__mkdir_p} %{buildroot}%{_mandir}/man3
install -pm0644 man/*.3 %{buildroot}%{_mandir}/man3/

%check
# The full target additionally mounts ext2 loop images and requires root.
# partcheck is upstream's maintained non-privileged syscall test subset.
set +e
CFLAGS="%{optflags}" \
  LDFLAGS="%{__global_ldflags}" \
%make_build partcheck
test_status=$?
set -e
# The suite deliberately creates mode-0400 fixtures throughout harness/.  Make
# all of its evidence readable even when a test fails, preserving its status.
chmod -R a+rX harness
exit "$test_status"

%files
%license COPYING
%doc ChangeLog README.md TODO
%{_libdir}/libaio.so.1*

%files devel
%license COPYING
%{_includedir}/libaio.h
%{_libdir}/libaio.so
%{_mandir}/man3/io*.3*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.113-1
- Initial openEuler RISC-V package with non-privileged upstream syscall tests.
