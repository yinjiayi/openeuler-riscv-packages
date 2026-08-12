# SPDX-License-Identifier: Apache-2.0
Name:           libotr
Version:        4.1.1
Release:        1%{?dist}
Summary:        Off-the-Record Messaging library and toolkit
License:        GPL-2.0-only AND LGPL-2.1-only
URL:            https://otr.cypherpunks.ca/
Source0:        libotr-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  make

%description
Libotr implements Off-the-Record Messaging encryption, authentication,
deniability, and forward secrecy, and includes command-line OTR tools.

%package devel
Summary:        Development files for libotr
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libgcrypt-devel

%description devel
Headers, pkg-config metadata, and the unversioned library link for developing
applications with libotr.

%prep
%autosetup -p1
# Fedora 44 carries this declaration-only fix so the complete Linux regression
# client compiles with modern C compilers. It does not alter test behavior.
sed -i '/#include <sys\/types.h>/a #include <sys/socket.h>' \
  tests/regression/client/client.c

%build
%configure \
  --disable-rpath \
  --disable-static \
  --with-pic
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README Protocol-v3.html
%{_bindir}/otr_*
%{_libdir}/libotr.so.5*
%{_mandir}/man1/otr_toolkit.1*

%files devel
%doc ChangeLog UPGRADING
%{_includedir}/libotr/
%{_libdir}/libotr.so
%{_libdir}/pkgconfig/libotr.pc
%{_datadir}/aclocal/libotr.m4

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.1-1
- Initial openEuler RISC-V package with the complete Linux upstream tests.
