# SPDX-License-Identifier: Apache-2.0
Name:           libwslay
Version:        1.1.1
Release:        2%{?dist}
Summary:        Lightweight WebSocket protocol library in C
License:        MIT
URL:            https://tatsuhiro-t.github.io/wslay/
Source0:        wslay-release-%{version}.tar.gz
Source1:        wslay-%{version}.tar.xz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  CUnit-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf

%description
Wslay implements WebSocket protocol version 13 with event-based and
frame-based low-level C APIs. It handles the data-transfer portion of the
protocol and leaves the HTTP opening handshake to applications.

%package devel
Summary:        Development files for libwslay
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned shared-library link for
developing applications with libwslay.

%package static
Summary:        Static library for libwslay
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The static libwslay library for applications that require static linking.

%prep
%autosetup -p1 -n wslay-release-%{version} -a 1
# The tag archive retains the complete test sources but not the generated
# manual pages.  Import only those generated pages from the matching official
# release asset so the Autotools build remains complete without Sphinx.
mv wslay-%{version}/doc/man doc/

%build
autoreconf -fiv
%configure --enable-shared --enable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libwslay.la

%check
# The Automake harness exercises the release-distribution test target.
%make_build check

# The release tag also ships a broader CMake/CUnit suite covering frame,
# event, queue, session, and stack behavior. Run it without installing the
# CMake-built library, whose install rules are not used by this package.
%{__cmake} -S . -B cmake-full-tests \
  -DWSLAY_CONFIGURE_INSTALL=OFF \
  -DWSLAY_EXAMPLES=OFF \
  -DWSLAY_SHARED=OFF \
  -DWSLAY_STATIC=ON \
  -DWSLAY_TESTS=ON
%{__cmake} --build cmake-full-tests --parallel 2
ctest --test-dir cmake-full-tests --output-on-failure

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libwslay.so.0*

%files devel
%license COPYING
%{_includedir}/wslay/
%{_libdir}/libwslay.so
%{_libdir}/pkgconfig/libwslay.pc
%{_mandir}/man3/wslay*.3*

%files static
%{_libdir}/libwslay.a

%changelog
* Tue Sep 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-2
- Restore generated manual pages from the matching official release asset.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-1
- Initial openEuler RISC-V package with both complete upstream test harnesses.
