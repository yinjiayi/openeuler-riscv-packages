# SPDX-License-Identifier: Apache-2.0
Name:           libqb
Version:        2.0.10
Release:        1%{?dist}
Summary:        High-performance logging, tracing, IPC, and poll library
License:        LGPL-2.1-or-later
URL:            https://github.com/ClusterLabs/libqb
Source0:        libqb-%{version}.tar.xz

BuildRequires:  check-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  pkgconf

%description
libqb provides high-performance client-server IPC, logging, tracing, polling,
and reusable container utilities for clustered applications.

%package devel
Summary:        Development files for libqb
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for developing
applications with libqb.

%package -n doxygen2man
Summary:        Convert Doxygen XML into manual pages
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n doxygen2man
doxygen2man converts Doxygen XML output into formatted manual pages.

%package help
Summary:        Documentation for libqb
BuildArch:      noarch

%description help
Manual page and upstream release documentation for libqb.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-slow-tests
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libqb.la
rm -rf -- %{buildroot}%{_docdir}/libqb

%check
%make_build check

%files
%license COPYING
%{_libdir}/libqb.so.100*
%{_sbindir}/qb-blackbox

%files devel
%license COPYING
%{_includedir}/qb/
%{_libdir}/libqb.so
%{_libdir}/pkgconfig/libqb.pc

%files -n doxygen2man
%license COPYING
%{_bindir}/doxygen2man
%{_mandir}/man1/doxygen2man.1*

%files help
%license COPYING
%doc ChangeLog INSTALL README.markdown
%{_mandir}/man8/qb-blackbox.8*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.10-1
- Update libqb while preserving libqb.so.100 and running all 12 upstream tests.
