# SPDX-License-Identifier: Apache-2.0
Name:           libffi
Version:        3.8.0
Release:        1%{?dist}
Summary:        Portable foreign function interface library
License:        MIT
URL:            https://sourceware.org/libffi/
Source0:        libffi-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
libffi provides a portable, high-level interface for calling compiled
functions at run time when their argument and result types are not known at
compile time.

%package devel
Summary:        Development files for libffi
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, manual pages, and the unversioned library link
for developing applications with libffi.

%prep
%autosetup -p1

%build
%configure \
  --disable-multi-os-directory \
  --disable-static \
  --enable-shared
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license LICENSE
%doc ChangeLog README.md
%{_libdir}/libffi.so.8*

%files devel
%license LICENSE
%{_includedir}/ffi.h
%{_includedir}/ffitarget.h
%{_libdir}/libffi.so
%{_libdir}/pkgconfig/libffi.pc
%{_mandir}/man3/ffi*.3*
%{_infodir}/libffi.info*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.8.0-1
- Initial openEuler RISC-V package with upstream architecture tests.
