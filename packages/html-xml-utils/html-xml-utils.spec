# SPDX-License-Identifier: Apache-2.0

Name:           html-xml-utils
Version:        8.8
Release:        1%{?dist}
Summary:        Utilities for manipulating HTML and XML files
License:        W3C AND BSD-3-Clause
URL:            https://www.w3.org/Tools/HTML-XML-utils/
Source0:        html-xml-utils-%{version}.tar.gz

BuildRequires:  bison
BuildRequires:  coreutils
BuildRequires:  curl-devel
BuildRequires:  diffutils
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gperf
BuildRequires:  grep
BuildRequires:  libidn-devel
BuildRequires:  libidn2-devel
BuildRequires:  make
BuildRequires:  nmap
BuildRequires:  sed

%description
html-xml-utils is a collection of command-line programs for manipulating and
converting HTML and XML documents. It includes tools for selection,
normalization, link processing, tables, inclusion, and entity conversion.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -rf -- %{buildroot}%{_docdir}/html-xml-utils

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/asc2xml
%{_bindir}/hx*
%{_bindir}/xml2asc
%{_mandir}/man1/asc2xml.1*
%{_mandir}/man1/hx*.1*
%{_mandir}/man1/xml2asc.1*

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 8.8-1
- Initial openEuler RISC-V package with the complete upstream test suite.
