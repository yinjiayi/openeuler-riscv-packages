# SPDX-License-Identifier: Apache-2.0

Name:           liboggz
Version:        1.1.3
Release:        1%{?dist}
Summary:        Ogg container inspection and authoring library
License:        BSD-3-Clause
URL:            https://www.xiph.org/oggz/
Source0:        liboggz-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libogg-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
liboggz provides a simple programming interface for reading, writing,
seeking, and validating Ogg bitstreams.

%package tools
Summary:        Command-line tools for inspecting and editing Ogg streams
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Utilities for chopping, dumping, validating, merging, scanning, and otherwise
inspecting Ogg bitstreams with liboggz.

%package devel
Summary:        Development files for liboggz
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libogg-devel%{?_isa}
Requires:       pkgconf-pkg-config

%description devel
Headers, the unversioned shared-library link, and pkg-config metadata for
developing applications with liboggz.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/liboggz.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/liboggz.so.2*

%files tools
%license COPYING
%{_bindir}/oggz*
%{_mandir}/man1/oggz*.1*

%files devel
%license COPYING
%{_includedir}/oggz/
%{_libdir}/liboggz.so
%{_libdir}/pkgconfig/oggz.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.3-1
- Initial openEuler RISC-V package with all 24 registered upstream tests.
