# SPDX-License-Identifier: Apache-2.0
Name:           libusb
Version:        1.0.30
Release:        1%{?dist}
Summary:        Library for USB device access
License:        LGPL-2.1-or-later
URL:            https://libusb.info/
Source0:        libusb-1.0.30.tar.bz2

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  systemd-devel


%description
libusb is a cross-platform library that provides user-space applications
with access to USB devices.

%package devel
Summary:        Development files for libusb
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned library link for developing
applications that use libusb.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-examples-build \
  --enable-tests-build
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS README ChangeLog
%{_libdir}/libusb-1.0.so.0*

%files devel
%license COPYING
%{_includedir}/libusb-1.0/
%{_libdir}/libusb-1.0.so
%{_libdir}/pkgconfig/libusb-1.0.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.30-1
- Initial openEuler RISC-V package with upstream regression tests.
