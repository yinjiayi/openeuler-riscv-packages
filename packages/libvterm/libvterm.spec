# SPDX-License-Identifier: Apache-2.0
Name:           libvterm
Version:        0.3.3
Release:        1%{?dist}
%global upstream_commit 9d6d2112335080312ef8c36667fa717ded4f7daf
Summary:        Abstract VT220/xterm/ECMA-48 terminal emulator library
License:        MIT
URL:            https://www.leonerd.org.uk/code/libvterm/
Source0:        libvterm-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  pkgconf

%description
libvterm is an abstract C library implementing a VT220, xterm, and ECMA-48
compatible terminal emulator. It provides parser, state, and screen layers.

%package devel
Summary:        Development files for libvterm
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for developing
applications with libvterm.

%prep
%autosetup -n libvterm-%{upstream_commit} -p1

%build
%make_build \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir}

%install
%make_install \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir}
rm -f %{buildroot}%{_libdir}/libvterm.la

%check
%make_build test \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir}

%files
%license LICENSE
%{_bindir}/unterm
%{_bindir}/vterm-ctrl
%{_bindir}/vterm-dump
%{_libdir}/libvterm.so.0*

%files devel
%license LICENSE
%{_includedir}/vterm.h
%{_includedir}/vterm_keycodes.h
%{_libdir}/libvterm.so
%{_libdir}/pkgconfig/vterm.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-1
- Initial openEuler RISC-V package with the complete upstream test corpus.
