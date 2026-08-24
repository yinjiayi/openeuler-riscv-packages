# SPDX-License-Identifier: Apache-2.0
Name:           mxml
Version:        4.0.5
Release:        1%{?dist}
Summary:        Small XML parsing and serialization library
License:        Apache-2.0 WITH mxml-exception
URL:            https://www.msweet.org/mxml/
Source0:        mxml-4.0.5.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Mini-XML is a small C library for reading, writing, and manipulating XML data.

%package devel
Summary:        Development files for Mini-XML
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files, pkg-config metadata, manual pages, and the unversioned shared
library link for developing applications with Mini-XML.

%prep
%autosetup -p1

%build
%set_build_flags
%configure --disable-static
%make_build

%install
%make_install
rm -rf %{buildroot}%{_docdir}/mxml4

%check
# Upstream's maintained target runs all file, string, and descriptor tests.
%make_build test

%files
%license LICENSE NOTICE
%doc CHANGES.md README.md
%{_libdir}/libmxml4.so.2*

%files devel
%license LICENSE NOTICE
%{_includedir}/mxml.h
%{_libdir}/libmxml4.so
%{_libdir}/pkgconfig/mxml4.pc
%{_mandir}/man3/mxml4.3*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0.4-1
- Initial openEuler RISC-V package with the complete upstream test target.
