# SPDX-License-Identifier: Apache-2.0
Name:           yajl
Version:        2.1.0
Release:        1%{?dist}
Summary:        Yet Another JSON Library
License:        ISC
URL:            https://github.com/lloyd/yajl
Source0:        yajl-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
YAJL is a small event-driven JSON parser and generator written in C. This
package also provides command-line JSON validation and reformatting tools.

%package devel
Summary:        Development files for YAJL
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned shared-library link for
developing applications with YAJL.

%prep
%autosetup -p1

%build
%cmake_conf -DLIB_SUFFIX=64
%cmake_build

%install
%cmake_install
rm -f %{buildroot}%{_libdir}/libyajl_s.a
install -d %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}%{_datadir}/pkgconfig/yajl.pc \
  %{buildroot}%{_libdir}/pkgconfig/yajl.pc

%check
%cmake_build --target test
%cmake_build --target test-api

%files
%license COPYING
%doc ChangeLog README TODO
%{_bindir}/json_reformat
%{_bindir}/json_verify
%{_libdir}/libyajl.so.2*

%files devel
%license COPYING
%{_includedir}/yajl/
%{_libdir}/libyajl.so
%{_libdir}/pkgconfig/yajl.pc

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.0-1
- Initial openEuler RISC-V package based on Fedora 44 and corroborating release evidence.
