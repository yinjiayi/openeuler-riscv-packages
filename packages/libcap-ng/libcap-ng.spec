# SPDX-License-Identifier: Apache-2.0
Name:           libcap-ng
Version:        0.9.5
Release:        1%{?dist}
Summary:        Alternate POSIX capabilities library
License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://github.com/stevegrubb/libcap-ng
Source0:        v0.9.5.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
libcap-ng provides a high-level interface for querying and manipulating Linux
process and file capabilities. This package also includes capability-inspection
utilities.

%package devel
Summary:        Development files for libcap-ng
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The public header, pkg-config metadata, manual pages, and unversioned shared
library links for developing applications with libcap-ng.

%prep
%autosetup -p1
touch NEWS
autoreconf -fi

%build
%configure \
  --disable-static \
  --disable-cap-audit \
  --disable-deprecated \
  --without-python3
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
rm -f %{buildroot}%{_datadir}/bash-completion/completions/cap-audit

%check
%make_build check

%files
%license COPYING COPYING.LIB
%doc AUTHORS ChangeLog README.md
%{_bindir}/filecap
%{_bindir}/netcap
%{_bindir}/pscap
%{_libdir}/libcap-ng.so.0*
%{_libdir}/libdrop_ambient.so.0*
%{_mandir}/man7/libdrop_ambient.7*
%{_mandir}/man8/filecap.8*
%{_mandir}/man8/netcap.8*
%{_mandir}/man8/pscap.8*
%{_datadir}/bash-completion/completions/filecap
%{_datadir}/bash-completion/completions/libcap-ng.bash_completion
%{_datadir}/bash-completion/completions/netcap
%{_datadir}/bash-completion/completions/pscap

%files devel
%license COPYING.LIB
%{_includedir}/cap-ng.h
%{_libdir}/libcap-ng.so
%{_libdir}/libdrop_ambient.so
%{_libdir}/pkgconfig/libcap-ng.pc
%{_datadir}/aclocal/cap-ng.m4
%{_mandir}/man3/*.3*

%changelog
* Mon Aug 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.5-1
- Follow the upstream bash-completion layout and omit the disabled cap-audit alias.

* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.2-1
- Initial openEuler RISC-V package from Fedora 44 identity and official upstream evidence.
