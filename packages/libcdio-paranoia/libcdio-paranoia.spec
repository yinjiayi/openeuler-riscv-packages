# SPDX-License-Identifier: Apache-2.0
Name:           libcdio-paranoia
Version:        10.2+2.0.2
Release:        1%{?dist}
Summary:        CD paranoia extraction libraries and tool using libcdio
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/libcdio/
Source0:        libcdio-paranoia-%{version}.tar.bz2

BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext-devel
BuildRequires:  libcdio-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  pkgconf

%description
Libcdio-paranoia reads Compact Disc Digital Audio through libcdio and
provides error-correcting extraction libraries and the cd-paranoia tool.

%package devel
Summary:        Development files for libcdio-paranoia
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libcdio-devel

%description devel
Headers, pkg-config metadata, and unversioned library links for applications
that use libcdio CDDA and paranoia interfaces.

%prep
%autosetup -p1
# Fedora 44's upstream-PR-52 guards prevent fclose(NULL) on failed log opens.
sed -i 's/fclose(logfile);/if (logfile) fclose(logfile);/' src/cd-paranoia.c
sed -i 's/fclose(reportfile);/if (reportfile) fclose(reportfile);/' src/cd-paranoia.c

%build
%configure \
  --disable-rpath \
  --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS NEWS.md README.md THANKS
%{_bindir}/cd-paranoia
%{_libdir}/libcdio_cdda.so.2*
%{_libdir}/libcdio_paranoia.so.2*
%{_mandir}/man1/cd-paranoia.1*
%lang(ja) %{_mandir}/ja/man1/cd-paranoia.1*

%files devel
%doc doc/overlapdef.txt
%{_includedir}/cdio/paranoia/
%{_libdir}/libcdio_cdda.so
%{_libdir}/libcdio_paranoia.so
%{_libdir}/pkgconfig/libcdio_cdda.pc
%{_libdir}/pkgconfig/libcdio_paranoia.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 10.2+2.0.2-1
- Update the target package with the complete upstream regression suite.
