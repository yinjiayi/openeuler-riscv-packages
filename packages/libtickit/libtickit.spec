# SPDX-License-Identifier: Apache-2.0
Name:           libtickit
Version:        0.4.6
Release:        1%{?dist}
Summary:        Terminal Interface Construction Kit
License:        MIT AND LicenseRef-wcwidth
URL:            https://www.leonerd.org.uk/code/libtickit/
Source0:        libtickit-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Test-Harness
BuildRequires:  pkgconf
BuildRequires:  libtermkey-devel
BuildRequires:  unibilium-devel >= 1.1.0
BuildRequires:  ncurses-base
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  glibc-devel
BuildRequires:  binutils

%description
libtickit provides an abstract C interface for constructing interactive
full-screen terminal programs. It includes terminal input and output handling,
render buffers, windows, pens, and event-loop integration.

%package devel
Summary:        Development files for libtickit
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf
Requires:       libtermkey-devel
Requires:       unibilium-devel >= 1.1.0

%description devel
Public headers, pkg-config metadata, shared-library linker name, static archive,
and the complete API manuals for developing applications with libtickit.

%prep
%autosetup -p1

%build
%make_build \
    CFLAGS='%{build_cflags}' \
    LDFLAGS='%{build_ldflags}' \
    PREFIX=%{_prefix} \
    LIBDIR=%{_libdir}

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
# Filter only installed libtool metadata; retain the static and shared APIs.
rm -f %{buildroot}%{_libdir}/libtickit.la

%check
# Run all original TAP tests, preserving upstream's own conditional skips.
%make_build test \
    CFLAGS='%{build_cflags}' \
    LDFLAGS='%{build_ldflags}' \
    PREFIX=%{_prefix} \
    LIBDIR=%{_libdir}

%files
%license LICENSE src/unicode.h
%doc README.md CHANGES CREDITS CODE-MAP
%{_libdir}/libtickit.so.3*

%files devel
%license LICENSE src/unicode.h
%{_includedir}/tickit.h
%{_includedir}/tickit-evloop.h
%{_includedir}/tickit-mockterm.h
%{_includedir}/tickit-termdrv.h
%{_libdir}/libtickit.so
%{_libdir}/libtickit.a
%{_libdir}/pkgconfig/tickit.pc
%{_mandir}/man3/tickit*.3*
%{_mandir}/man7/tickit*.7*

%changelog
* Tue Oct 20 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.6-1
- Initial package retaining default shared/static APIs and the full TAP suite.
- Preserve the MIT license and complete embedded wcwidth notice.
