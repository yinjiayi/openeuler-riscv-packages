# SPDX-License-Identifier: Apache-2.0
Name:           libassuan
Version:        3.0.2
Release:        1%{?dist}
Summary:        IPC library used by GnuPG components
License:        GPL-3.0-or-later AND LGPL-2.1-or-later AND LGPL-3.0-or-later
URL:            https://gnupg.org/related_software/libassuan/
Source0:        libassuan-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  gawk
BuildRequires:  libgpg-error-devel >= 1.17
BuildRequires:  make

%description
Libassuan implements the Assuan IPC protocol used by GnuPG, GPGME, and
related applications. This source release carries a new shared-library ABI.

%package -n libassuan9
Summary:        Assuan IPC runtime library with SONAME 9

%description -n libassuan9
The libassuan.so.9 runtime library. It is parallel-installable with the
libassuan.so.0 ABI shipped by the openEuler target repository.

%package devel
Summary:        Development files for libassuan
Requires:       libassuan9%{?_isa} = %{version}-%{release}
Requires:       libgpg-error-devel%{?_isa} >= 1.17
Requires:       pkgconfig

%description devel
Headers, configuration metadata, and unversioned library links for developing
applications against the current libassuan ABI.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --includedir=%{_includedir}/libassuan3
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files -n libassuan9
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README
%{_libdir}/libassuan.so.9*

%files devel
%{_bindir}/libassuan-config
%{_includedir}/libassuan3/
%{_libdir}/libassuan.so
%{_libdir}/pkgconfig/libassuan.pc
%{_datadir}/aclocal/libassuan.m4
%{_infodir}/assuan.info*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.2-1
- Initial openEuler RISC-V package with parallel SONAME 9 runtime.
