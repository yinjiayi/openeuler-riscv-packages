# SPDX-License-Identifier: Apache-2.0
Name:           zvbi
Version:        0.2.45
Release:        3%{?dist}
Summary:        Raw VBI, Teletext, and Closed Caption decoding library
License:        GPL-2.0-or-later AND LGPL-2.0-or-later AND LGPL-2.1-or-later AND BSD-2-Clause AND MIT
URL:            https://github.com/zapping-vbi/zvbi
Source0:        zvbi-0.2.45.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  gettext-devel
BuildRequires:  libICE-devel
BuildRequires:  libpng-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  tzdata

%description
ZVBI captures and decodes vertical-blanking-interval data such as Teletext,
closed captions, and broadcast signalling carried in analog television
signals.

%package devel
Summary:        Development files for ZVBI
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, unversioned shared-library links, and pkg-config metadata for
developing applications with ZVBI.

%prep
%autosetup -n zvbi-%{version} -p1

%build
./autogen.sh
%configure \
  --disable-rpath \
  --without-doxygen \
  --disable-static \
  --enable-v4l \
  --enable-dvb \
  --enable-proxy \
  --enable-tests \
  --enable-examples
%make_build

%install
%make_install
%find_lang %{name}
find %{buildroot} -name '*.a' -delete
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files -f %{name}.lang
%license COPYING.md
%doc AUTHORS BUGS ChangeLog NEWS README.md TODO
%{_bindir}/zvbi*
%if "%{_sbindir}" != "%{_bindir}"
%{_sbindir}/zvbid
%endif
%{_libdir}/libzvbi.so.0*
%{_libdir}/libzvbi-chains.so.0*
%{_mandir}/man1/zvbi*1*

%files devel
%{_includedir}/libzvbi.h
%{_libdir}/libzvbi.so
%{_libdir}/libzvbi-chains.so
%{_libdir}/pkgconfig/zvbi-0.2.pc

%changelog
* Tue Sep 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.45-3
- Disable optional, unpackaged Doxygen output to bound the dependency closure.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.45-2
- Use the verified 0.2.45 archive root and synchronize update metadata and smoke coverage.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.44-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
