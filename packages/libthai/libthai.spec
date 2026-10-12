# SPDX-License-Identifier: Apache-2.0
Name:           libthai
Version:        0.1.30
Release:        1%{?dist}
Summary:        Thai language support library
License:        LGPL-2.1-or-later
URL:            https://linux.thai.net/projects/libthai
Source0:        libthai-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libdatrie-devel
BuildRequires:  make
BuildRequires:  pkgconf

%description
libthai provides Thai character classification, word breaking, input
validation, collation, and text rendering support.

%package devel
Summary:        Development files for libthai
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libdatrie-devel%{?_isa}

%description devel
Headers, pkg-config metadata, and the unversioned shared-library link for
developing applications with libthai.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-doxygen-doc
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libthai.la

%check
# Run all maintained tests with the generated Thai word-break dictionary.
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libthai.so.0*
%{_datadir}/libthai/thbrk.tri

%files devel
%license COPYING
%{_includedir}/thai/
%{_libdir}/libthai.so
%{_libdir}/pkgconfig/libthai.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.30-1
- Update the openEuler RISC-V package to 0.1.30 with all upstream tests.
