# SPDX-License-Identifier: Apache-2.0
Name:           raptor2
Version:        2.0.16
Release:        1%{?dist}
Summary:        RDF parser and serializer toolkit
License:        Apache-2.0 OR GPL-2.0-or-later OR LGPL-2.1-or-later
URL:            https://librdf.org/raptor/
Source0:        raptor2-%{version}.tar.gz
Patch0:         0001-libxml2-2.11-private-entity-fields.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libcurl-devel
BuildRequires:  libicu-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  yajl-devel

%description
Raptor is a C toolkit for parsing and serializing RDF syntax families,
including RDF/XML, Turtle, N-Triples, N-Quads, TriG, RDFa, RSS, and JSON.
It also provides the rapper command-line parser utility.

%package devel
Summary:        Development files for Raptor 2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, API documentation, and the unversioned library
link for developing applications with Raptor 2.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-parsers=all \
  --enable-release \
  --enable-serializers=all \
  --with-www=curl \
  --with-yajl=yes
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libraptor2.la

%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion raptor2)" = "%{version}"
# Run every upstream unit and parser/serializer fixture target unchanged.
%make_build check

%files
%license COPYING COPYING.LIB LICENSE-2.0.txt LICENSE.txt NOTICE
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/rapper
%{_libdir}/libraptor2.so.0*
%{_mandir}/man1/rapper.1*

%files devel
%license COPYING COPYING.LIB LICENSE-2.0.txt LICENSE.txt NOTICE
%doc UPGRADING.html
%{_includedir}/raptor2/
%{_libdir}/libraptor2.so
%{_libdir}/pkgconfig/raptor2.pc
%{_mandir}/man3/libraptor2.3*
%{_datadir}/gtk-doc/html/raptor2/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.16-1
- Upgrade the target raptor2 ABI-compatible package to current upstream stable.
