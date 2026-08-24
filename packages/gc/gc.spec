# SPDX-License-Identifier: Apache-2.0
Name:           gc
Version:        8.2.12
Release:        1%{?dist}
Summary:        Conservative garbage collector for C and C++
License:        HPND
URL:            https://www.hboehm.info/gc/
Source0:        gc-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
The Boehm-Demers-Weiser collector provides conservative garbage collection
for C and C++ programs.

%package devel
Summary:        Development files for the Boehm collector
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, library links, and pkg-config metadata for gc.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-cplusplus
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license README.QUICK
%doc ChangeLog
%{_docdir}/gc/AUTHORS
%{_docdir}/gc/README*
%{_docdir}/gc/[a-z]*.md
%{_libdir}/libcord.so.1*
%{_libdir}/libgc.so.1*
%{_libdir}/libgccpp.so.1*
%{_libdir}/libgctba.so.1*

%files devel
%{_includedir}/gc.h
%{_includedir}/gc_cpp.h
%{_includedir}/gc/
%{_libdir}/libcord.so
%{_libdir}/libgc.so
%{_libdir}/libgccpp.so
%{_libdir}/libgctba.so
%{_libdir}/pkgconfig/bdw-gc.pc
%{_mandir}/man3/gc.3*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 8.2.12-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
