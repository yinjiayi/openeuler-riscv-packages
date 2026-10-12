# SPDX-License-Identifier: Apache-2.0
Name:           libfreeaptx
Version:        0.2.2
Release:        1%{?dist}
%global upstream_commit 6dee419f934ec781e531f885f7e8e740752e67d1
Summary:        Open-source aptX and aptX HD audio codec
License:        LGPL-2.1-or-later
URL:            https://github.com/regularhunter/libfreeaptx
Source0:        libfreeaptx-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf

%description
libfreeaptx is an open-source implementation of aptX and aptX HD for raw
24-bit stereo PCM audio. The package also provides encoder and decoder tools.

%package devel
Summary:        Development files for libfreeaptx
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Public header, pkg-config metadata, and unversioned shared-library link for
developing applications with libfreeaptx.

%prep
%autosetup -n libfreeaptx-%{upstream_commit} -p1

%build
%make_build CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}" \
  PREFIX=%{_prefix} LIBDIR=%{_lib} INCDIR=include

%install
%make_install CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}" \
  PREFIX=%{_prefix} LIBDIR=%{_lib} INCDIR=include

%check
# Upstream 0.2.2 has no test target. Exercise both codec modes end to end.
dd if=/dev/zero of=check.s24le bs=24 count=10 status=none
LD_LIBRARY_PATH="$PWD${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ./freeaptxenc <check.s24le >check.aptx
LD_LIBRARY_PATH="$PWD${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ./freeaptxdec <check.aptx >check.standard.s24le
test -s check.aptx
test "$(wc -c <check.standard.s24le)" -eq 240
LD_LIBRARY_PATH="$PWD${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ./freeaptxenc --hd <check.s24le >check.aptxhd
LD_LIBRARY_PATH="$PWD${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ./freeaptxdec --hd <check.aptxhd >check.hd.s24le
test -s check.aptxhd
test "$(wc -c <check.hd.s24le)" -eq 240

%files
%license COPYING
%doc README
%{_bindir}/freeaptxenc
%{_bindir}/freeaptxdec
%{_libdir}/libfreeaptx.so.0*

%files devel
%license COPYING
%{_includedir}/freeaptx.h
%{_libdir}/libfreeaptx.so
%{_libdir}/pkgconfig/libfreeaptx.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.2-1
- Initial package from the official SHA-256-pinned libfreeaptx 0.2.2 source.
