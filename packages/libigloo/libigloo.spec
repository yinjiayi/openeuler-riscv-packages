# SPDX-License-Identifier: Apache-2.0
Name:           libigloo
Version:        0.9.5
Release:        1%{?dist}
Summary:        Common C framework used by the Icecast project
License:        LGPL-2.0-or-later
URL:            https://gitlab.xiph.org/xiph/icecast-libigloo
Source0:        libigloo-v%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  rhash-devel

%description
libigloo provides common C facilities used by Icecast, including typed
objects, feature detection, digests, UUIDs, and a TAP test framework.

%package devel
Summary:        Development files for libigloo
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The public headers, pkg-config metadata, and linker name for libigloo.

%prep
%autosetup -n icecast-libigloo-v%{version}

%build
./autogen.sh
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# The full upstream Automake TESTS list contains ten TAP suites.
%make_build check

%files
%license COPYING
%doc NEWS README
%{_libdir}/libigloo.so.0*

%files devel
%license COPYING
%{_includedir}/igloo/
%{_libdir}/libigloo.so
%{_libdir}/pkgconfig/igloo.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.5-1
- Package official libigloo with all ten upstream TAP suites.
