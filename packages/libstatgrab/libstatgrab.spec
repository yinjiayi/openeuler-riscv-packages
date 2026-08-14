# SPDX-License-Identifier: Apache-2.0
Name:           libstatgrab
Version:        0.92.1
Release:        1%{?dist}
Summary:        Cross-platform library for system statistics
License:        LGPL-2.1-or-later
URL:            https://libstatgrab.org/
Source0:        libstatgrab-0.92.1.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  perl

%description
libstatgrab is a C library providing cross-platform access to statistics
about the system on which it runs. It also includes the statgrab and saidar
monitoring utilities.

%package devel
Summary:        Development files for libstatgrab
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the shared linker name, and pkg-config metadata for applications
using libstatgrab.

%package -n statgrab
Summary:        Command-line statistics interface from libstatgrab
License:        GPL-2.0-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n statgrab
The statgrab command-line interface exposes system statistics in a
sysctl-style format and includes MRTG helper scripts.

%package -n saidar
Summary:        Curses system monitor from libstatgrab
License:        GPL-2.0-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n saidar
saidar is a curses-based real-time view of system statistics.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --without-log4cplus \
  --disable-examples \
  --enable-tests=yes
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.la' -delete
rm -rf -- %{buildroot}%{_docdir}/libstatgrab

%check
# The generated TAP cases share a harness; run the complete upstream matrix
# serially so result numbering remains valid under QEMU.
make -j1 check

%files
%license COPYING.LGPL
%{_libdir}/libstatgrab.so.10*

%files devel
%doc AUTHORS NEWS PLATFORMS README
%{_includedir}/statgrab.h
%{_libdir}/libstatgrab.so
%{_libdir}/pkgconfig/libstatgrab.pc
%{_mandir}/man3/*

%files -n statgrab
%license COPYING
%{_bindir}/statgrab
%{_bindir}/statgrab-make-mrtg-config
%{_bindir}/statgrab-make-mrtg-index
%{_mandir}/man1/statgrab*

%files -n saidar
%license COPYING
%{_bindir}/saidar
%{_mandir}/man1/saidar.1*

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.92.1-1
- Initial openEuler RISC-V package with the complete upstream test suite.
