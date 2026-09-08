# SPDX-License-Identifier: Apache-2.0
Name:           ivykis
Version:        0.43.2
Release:        1%{?dist}
Summary:        Portable asynchronous I/O readiness notification library
License:        LGPL-2.1-only
URL:            https://github.com/buytenh/ivykis
Source0:        ivykis-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
ivykis is a portable event-dispatching library for file descriptors, timers,
signals, tasks, and worker threads.

%package devel
Summary:        Development files for ivykis
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, manual pages, and the unversioned library link
for developing applications with ivykis.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libivykis.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS DEDICATION
%{_libdir}/libivykis.so.0*

%files devel
%license COPYING
%{_includedir}/iv*.h
%{_libdir}/libivykis.so
%{_libdir}/pkgconfig/ivykis.pc
%{_mandir}/man3/*.3*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.43.2-1
- Initial openEuler RISC-V package.
