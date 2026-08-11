# SPDX-License-Identifier: Apache-2.0
Name:           lzo
Version:        2.10
Release:        1%{?dist}
Summary:        Data compression library optimized for decompression speed
License:        GPL-2.0-or-later
URL:            https://www.oberhumer.com/opensource/lzo
Source0:        lzo-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
LZO is a portable lossless data-compression library designed for very fast
decompression and low memory overhead.

%package devel
Summary:        Development files for LZO
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned shared-library link for
developing applications with LZO 2.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-shared
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS
%{_libdir}/liblzo2.so.2*

%files devel
%license COPYING
%{_includedir}/lzo/
%{_libdir}/liblzo2.so
%{_libdir}/pkgconfig/lzo2.pc

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.10-1
- Initial openEuler RISC-V package based on cross-distribution release evidence.
