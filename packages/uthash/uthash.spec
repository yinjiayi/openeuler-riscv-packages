# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           uthash
Version:        2.3.0
Release:        1%{?dist}
Summary:        Hash table and utility headers for C
License:        BSD-1-Clause
URL:            https://troydhanson.github.io/uthash
Source0:        uthash-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl

%description
uthash provides single-header data structures for C, including hash tables,
linked lists, dynamic arrays, strings, ring buffers, and stacks.

%prep
%autosetup -p1

%build
# Header-only package; compilation is performed by the test suite.

%install
install -d %{buildroot}%{_includedir}
install -pm0644 src/utarray.h src/uthash.h src/utlist.h \
  src/utringbuffer.h src/utstack.h src/utstring.h \
  %{buildroot}%{_includedir}/

%check
%make_build -C tests tests_only \
  CC=%{__cc} \
  EXTRA_CFLAGS="%{optflags}"

%files
%license LICENSE
%doc README.md doc/ChangeLog.txt
%{_includedir}/utarray.h
%{_includedir}/uthash.h
%{_includedir}/utlist.h
%{_includedir}/utringbuffer.h
%{_includedir}/utstack.h
%{_includedir}/utstring.h

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.0-1
- Initial openEuler RISC-V header package based on cross-distribution evidence.
