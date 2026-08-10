# SPDX-License-Identifier: Apache-2.0
Name:           libhangul
Version:        0.2.0
Release:        1%{?dist}
Summary:        Korean Hangul input-method logic library
License:        LGPL-2.1-or-later
URL:            https://github.com/libhangul/libhangul
Source0:        libhangul-0.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  check-devel
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make


%description
libhangul implements Korean Hangul input-method composition and Hanja lookup.

%package devel
Summary:        Development files for libhangul
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and CMake metadata for developing applications with libhangul.

%prep
%autosetup -p1 -n libhangul-libhangul-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DENABLE_UNIT_TEST=ON
%cmake_build
%cmake_build --target unittest

%install
%cmake_install
%find_lang libhangul

%check
%ctest

%files -f libhangul.lang
%license COPYING
%doc README
%{_libdir}/libhangul.so.1*
%{_datadir}/libhangul/

%files devel
%license COPYING
%{_includedir}/hangul-1.0/
%{_libdir}/libhangul.so
%{_libdir}/cmake/libhangul/

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package.
