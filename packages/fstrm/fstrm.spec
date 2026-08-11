# SPDX-License-Identifier: Apache-2.0
Name:           fstrm
Version:        0.6.1
Release:        1%{?dist}
Summary:        Frame Streams data transport library and tools
License:        MIT
URL:            https://github.com/farsightsec/fstrm
Source0:        fstrm-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libevent-devel
BuildRequires:  libtool
BuildRequires:  make

%description
fstrm provides a C implementation of the Frame Streams protocol together
with capture, dump, and replay command-line utilities.

%package devel
Summary:        Development files for fstrm
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned library link for developing
applications with fstrm.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --disable-static --enable-programs
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libfstrm.la

%check
%make_build check

%files
%license LICENSE
%doc COPYRIGHT README.md
%{_bindir}/fstrm_capture
%{_bindir}/fstrm_dump
%{_bindir}/fstrm_replay
%{_libdir}/libfstrm.so.0*
%{_mandir}/man1/fstrm_capture.1*
%{_mandir}/man1/fstrm_dump.1*
%{_mandir}/man1/fstrm_replay.1*

%files devel
%license LICENSE
%{_includedir}/fstrm.h
%{_includedir}/fstrm/
%{_libdir}/libfstrm.so
%{_libdir}/pkgconfig/libfstrm.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.1-1
- Initial openEuler RISC-V package.
