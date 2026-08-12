# SPDX-License-Identifier: Apache-2.0

Name:           http-parser
Version:        2.9.4
Release:        4%{?dist}
Summary:        Fast streaming HTTP request and response parser
License:        MIT
URL:            https://github.com/nodejs/http-parser
Source0:        http-parser-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
http-parser is a compact, allocation-free streaming parser for HTTP requests
and responses, including chunked transfer encoding and protocol upgrades.

%package devel
Summary:        Development files for http-parser
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and linker name for developing applications with http-parser.

%prep
%autosetup -p1

%build
%make_build library \
  CFLAGS="%{optflags} -Wall -Wextra -Werror" \
  LDFLAGS="%{build_ldflags}"

%install
%make_install \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  CFLAGS="%{optflags} -Wall -Wextra -Werror" \
  LDFLAGS="%{build_ldflags}"

%check
%make_build test \
  CFLAGS="%{optflags} -Wall -Wextra -Werror" \
  LDFLAGS="%{build_ldflags}"

%files
%license LICENSE-MIT
%doc AUTHORS README.md
%{_libdir}/libhttp_parser.so.2.9*

%files devel
%{_includedir}/http_parser.h
%{_libdir}/libhttp_parser.so

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.9.4-4
- Preserve target EVR while retaining both complete upstream parser suites.
