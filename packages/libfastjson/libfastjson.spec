# SPDX-License-Identifier: Apache-2.0
Name:           libfastjson
Version:        1.2609.0
Release:        1%{?dist}
Summary:        Performance-focused JSON library for C
License:        MIT
URL:            https://github.com/rsyslog/libfastjson
Source0:        v1.2609.0.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
libfastjson is a performance-focused JSON parsing and serialization library.

%package devel
Summary:        Development files for libfastjson
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for developing with libfastjson.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libfastjson.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md
%{_libdir}/libfastjson.so.4*

%files devel
%license COPYING
%{_includedir}/libfastjson/
%{_libdir}/libfastjson.so
%{_libdir}/pkgconfig/libfastjson.pc

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2304.0-1
- Initial openEuler RISC-V package.

