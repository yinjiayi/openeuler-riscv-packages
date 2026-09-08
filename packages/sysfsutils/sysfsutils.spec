# SPDX-License-Identifier: Apache-2.0
Name:           sysfsutils
Version:        2.1.1
Release:        1%{?dist}
Summary:        Utilities and library for Linux sysfs
License:        GPL-2.0-only AND LGPL-2.1-or-later
URL:            https://github.com/linux-ras/sysfsutils
Source0:        sysfsutils-2.1.1.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
sysfsutils provides the systool utility and libsysfs for querying Linux sysfs.

%package devel
Summary:        Development files for libsysfs
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned library link for libsysfs.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libsysfs.la

%check
%make_build check

%files
%license COPYING cmd/GPL lib/LGPL
%doc AUTHORS CREDITS README
%{_bindir}/systool
%{_libdir}/libsysfs.so.2*
%{_mandir}/man1/systool.1*

%files devel
%{_includedir}/sysfs/
%{_libdir}/libsysfs.so
%{_libdir}/pkgconfig/libsysfs.pc

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.1-1
- Initial openEuler RISC-V package.
