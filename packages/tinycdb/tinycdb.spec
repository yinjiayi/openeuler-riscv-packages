# SPDX-License-Identifier: Apache-2.0
Name:           tinycdb
Version:        0.81
Release:        1%{?dist}
Summary:        Constant database library and tools
License:        MIT
URL:            https://www.corpit.ru/mjt/tinycdb.html
Source0:        tinycdb-%{version}.tar.gz

BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  make

%description
tinycdb provides a small, fast constant-database library and the cdb command
for creating, querying, listing, dumping, and inspecting CDB files.

%package devel
Summary:        Development files for tinycdb
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, static library, pkg-config metadata, manual, and unversioned linker
name for developing applications with tinycdb.

%prep
%autosetup -p1

%build
%make_build \
  CC=%{__cc} \
  CFLAGS='%{build_cflags}' \
  LDFLAGS='%{build_ldflags}' \
  static sharedlib

%install
%make_build DESTDIR=%{buildroot} \
  CC=%{__cc} \
  CFLAGS='%{build_cflags}' \
  LDFLAGS='%{build_ldflags}' \
  prefix=%{_prefix} \
  libdir=%{_libdir} \
  mandir=%{_mandir} \
  install-all install-sharedlib

%check
%make_build test
%make_build test-shared

%files
%license LICENSE
%doc NEWS
%{_bindir}/cdb
%{_libdir}/libcdb.so.1
%{_mandir}/man1/cdb.1*
%{_mandir}/man5/cdb.5*

%files devel
%license LICENSE
%{_includedir}/cdb.h
%{_libdir}/libcdb.a
%{_libdir}/libcdb.so
%{_libdir}/pkgconfig/libcdb.pc
%{_mandir}/man3/cdb.3*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.81-1
- Initial openEuler RISC-V package with upstream static and shared tests.
